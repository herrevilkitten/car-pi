import asyncio
import datetime

import obd

from gps3.agps3threaded import AGPS3mechanism
#from gps import *

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
        self.current_data = [{}]

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

    def handle_obd(self):
        if self.obd.is_connected() == False:
            return
        print("Querying OBD connection")

        current_data = {}

        for command in OBD_COMMANDS:
            current_data[command] = self.obd.query(command)

        print(current_data)
        return current_data

    def handle_gps(self):
        current_data = {}
        
        for field in GPS_FIELDS:
            current_data[field] = getattr(self.agps_thread.data_stream, field)
            
        print(current_data)
        return current_data

    def handle_interval(self):
        current_obd = self.handle_obd()
        current_gps = self.handle_gps()

        self.current_data.append({
            "timestamp": datetime.datetime.now()
            "obd": current_obd,
            "gps": current_gps
        })

        self.loop.call_later(GPS_INTERVALS, self.handle_interval)

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
