
"""
from gps3 import agps3
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect("localhost", 2947)
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print('Altitude  = ', data_stream.alt)
        print('Latitude  = ', data_stream.lat)
        print('Longitude = ', data_stream.lon)
"""
