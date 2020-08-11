import asyncio
import datetime
import sqlite3

import obd
from gps3.agps3threaded import AGPS3mechanism

OBD_COMMANDS = [
    obd.commands.RPM,
    obd.commands.SPEED,
    obd.commands.FUEL_STATUS,
    obd.commands.STATUS,
    obd.commands.INTAKE_TEMP,
    obd.commands.AIR_STATUS,
    obd.commands.FUEL_LEVEL,
    obd.commands.RELATIVE_ACCEL_POS,
    obd.commands.FUEL_RATE,
    obd.commands.FUEL_TYPE,
    obd.commands.ETHANOL_PERCENT,
    obd.commands.GET_DTC
]

GPS_FIELDS = [
    "time",
    "lat",
    "lon",
    "alt",
    "speed",
    "track"
]

GPS_INTERVALS = 5
OBD_INTERVALS = 30

class CarPi:
    def __init__(self, port):
        self.data = []
        self.port = port
        self.obd = None
        self.loop = None
        self.agps_thread = None
        self.current_data = []
        self.interval_count = 0
        self.sqlite = sqlite3.connect("car-pi.db")

    def start(self):
        self.obd = obd.Async(self.port)

        for command in OBD_COMMANDS:
            self.obd.watch(command)

        self.loop = asyncio.get_event_loop()

        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data(host='localhost', port=2947)
        self.agps_thread.run_thread()

        self.obd.start()
        self.loop.call_soon(self.handle_interval)
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.obd.stop()

    def init_database(self):
        try:
            cursor = self.sqlite.cursor()
            cursor.execute("""
CREATE TABLE IF NOT EXISTS CarPi_Entry (
    id INTEGER AUTOINCREMENT,
    timestamp STRING,
    latitude NUMBER,
    longitude NUMBER,
    altitude NUMBER,
    speed NUMBER,
    track NUMBER
)
        """)
            cursor.commit()
        except sqlite3.Error as e:
            print "An error occurred:", e.args[0]

    def handle_obd(self):
        if self.obd.is_connected() == False:
            return
        print("Querying OBD")

        current_data = {}

        for command in OBD_COMMANDS:
            current_data[command] = self.obd.query(command)

        return current_data

    def handle_gps(self):
        print("Querying GPS")
        current_data = {}
        
        for field in GPS_FIELDS:
            current_data[field] = getattr(self.agps_thread.data_stream, field)
            
        return current_data

    def record_data(self):
        print("Saving data")
        data = []
        for entry in self.current_data:
            data.append((
                entry["timestamp"].isoformat(),
                entry["gps"]["lat"],
                entry["gps"]["lon"],
                entry["gps"]["alt"],
                entry["gps"]["speed"],
                entry["gps"]["track"],
            ))

        try:
            cursor = self.sqlite.cursor()
            cursor.executemany("INSERT INTO CarPi_Entry VALUES (?, ?, ?, ?, ?, ?)", data)
            cursor.commit()
        except sqlite3.Error as e:
            print "An error occurred:", e.args[0]

    def handle_interval(self):
        self.interval_count = self.interval_count + 1
        current_obd = self.handle_obd()
        current_gps = self.handle_gps()

        self.current_data.append({
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "obd": current_obd,
            "gps": current_gps
        })

        print(self.current_data)
        self.loop.call_later(GPS_INTERVALS, self.handle_interval)

        if (self.interval_count % 60 == 0):
            self.record_data()

    # RPM
    # SPEED
    # FUEL_STATUS
    # STATUS
    # INTAKE_TEMP
    # AIR_STATUS
    # FUEL_LEVEL
    # RELATIVE_ACCEL_POS
    # OIL_TEMP
    # FUEL_RATE
    # FUEL_TYPE
    # ETHANOL_PERCENT
    # GET_DTC


if __name__ == "__main__":
    car_pi = CarPi("/dev/rfcomm0")
    car_pi.start()
