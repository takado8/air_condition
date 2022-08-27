from bme280.bme280 import readBME280All as read_bme
from DFRobot_ENS160.python.raspberrypi.examples.get_data import ENS160
from time import sleep
from service.logger import Logger


def get_bme_data():
    try:
        return read_bme()
    except Exception as ex:
        print('cannot get bme280 sensor data. Exception: ' + str(ex))


temp, pressure, humidity = get_bme_data()

try:
    if temp is not None and humidity is not None:
        ens = ENS160(temperature=temp, humidity=humidity)
    elif temp is not None:
        ens = ENS160(temperature=temp)
    else:
        ens = ENS160()
    ens.setup()
except Exception as ex:
    print('cannot initialize ENS160 sensor. Exception: ' + str(ex))
    ens = None

logger = Logger()

while True:
    temp, pressure, humidity = get_bme_data()
    aqi, vocs, co2, status = None, None, None, None
    if ens is not None:
        try:
            aqi, vocs, co2, status = ens.get_all_data(temperature=temp, humidity=humidity)
        except:
            pass
        print('Status: {}'.format(status))
        print('Air index: {}/5'.format(int(aqi)))
        print('VOCS: {}ppb'.format(int(vocs)))
        print('CO2: {}ppm'.format(int(co2)))
    print('Temperature: {:.1f}*C'.format(temp))
    print('Humidity: {:.1f}%'.format(humidity))
    print('Pressure: {:.2f}hPa\n'.format(pressure))
    logger.append_record({'temp': temp, 'pressure': pressure, 'humidity': humidity,
                          'aqi': aqi, 'vocs': vocs, 'co2': co2})
    sleep(10)
