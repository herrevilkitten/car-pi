import obd

connection = obd.OBD("/dev/rfcomm0") # auto-connects to USB or RF port
if (connection.is_connected()):
  cmd = obd.commands.SPEED # select an OBD command (sensor)
  response = connection.query(cmd) # send the command, and parse the response
  print(response.value) # returns unit-bearing values thanks to Pint
  print(response.value.to("mph")) # user-friendly unit conversions

  cmd = obd.commands.GET_DTC
  response = connection.query(cmd)
  print(response.value)
else:
  print("Not connected")
