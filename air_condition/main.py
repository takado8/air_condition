from bme280.bme280 import readBME280All as read_bme
from DFRobot_ENS160.python.raspberrypi.examples.get_data import ENS160
from time import sleep

def get_bme_data():
    try:
        return read_bme()
    except Exception as ex:
        print(ex)

temp, pressure, humidity = get_bme_data()
if temp != None and humidity != None:
    ens = ENS160(temperature=temp, humidity=humidity)
elif temp != None:    
    ens = ENS160(temperature=temp)
else:
    ens = ENS160()
ens.setup()

while True:
    temp, pressure, humidity = get_bme_data()
    
    aqi, vocs, co2 = ens.get_all_data(temperature=temp, humidity=humidity)

    print('Temperature: {:.2f}*C'.format(temp))
    print('Humidity: {:.2f}%'.format(humidity))
    print('Pressure: {:.2f}hPa'.format(pressure))
    print('Air index: {:.2f}/5'.format(aqi))
    print('VOCS: {:.2f}ppb'.format(vocs))
    print('CO2: {:.2f}ppm'.format(co2))

    sleep(1)