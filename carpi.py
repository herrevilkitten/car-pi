import asyncio
import datetime

import obd

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


class CarPi:
    def __init__(self, port):
        self.data = []
        self.port = port
        self.obd = None
        self.loop = None

    def start(self):
        self.obd = obd.Async(self.port)

        for command in OBD_COMMANDS:
            self.obd.watch(command)

        self.loop = asyncio.get_event_loop()

        self.obd.start()
        self.loop.call_soon(self.handle_interval)
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.obd.stop()

    def handle_interval(self):
        if self.obd.is_connected() == False:
            self.loop.call_later(5, self.handle_interval)
            return
        print("Querying OBD connection")

        current_data = {
            "timestamp": datetime.datetime.now()
        }

        for command in OBD_COMMANDS:
            current_data[command] = self.obd.query(command)

        self.loop.call_later(60, self.handle_interval)

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
