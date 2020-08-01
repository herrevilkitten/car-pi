# car-pi

## Hardware

### Stage 1 - ODBII
https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/

$35

https://smile.amazon.com/gp/product/B07N38B86S/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1

$30

https://smile.amazon.com/gp/product/B005NLQAHS/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1

$25

* Query OBD about 1/minute
  * RPM, MPH, Gas/Battery, Diagnostics Codes
* Store results locally until a network connection is detected
  * How to do this in python?

Begin insertion into database.

* Use a service (Heroku, AWS, GCP, etc.) to insert stuff into a database (Salesforce, S3, GCP, etc.)
* A web service/app to view the data in a convenient format
* Analytics?

### Stage 2 - GPS

https://smile.amazon.com/gp/product/B008200LHW/ref=ox_sc_saved_title_2?smid=ATVPDKIKX0DER&psc=1

$25

https://www.amazon.com/MPU-6050-MPU6050-Accelerometer-Gyroscope-Converter/dp/B008BOPN40/

$6

### Stage 3 - Gas/Battery

Monitor the Gas/Battery level and warn the driver if it gets low.

Open a map and route to the nearest refuel place.

### Stage ??? - CAN interface

The CAN (Controller Area Network) interface is a real-time interface that gets you access to some interesting things, like how far the steering wheel is turned.  Difficulty: may not be able to do diagnostics and CAN at the same time.

## Software

### Raspbian

### Python

### gpsd

## Services

### Mapping

https://www.openstreetmap.org/#map=4/38.01/-95.84

### Weather

https://openweathermap.org/price
