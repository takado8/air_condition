from bme280.bme280 import readBME280All as read_bme
from DFRobot_ENS160.python.raspberrypi.examples.get_data import ENS160
from time import sleep
from service.logger import Logger
from collections import deque


INTERVAL = 5


def get_avg(collection):
    return sum(collection) / len(collection)


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

SLEEP_TIME = 5
SECONDS_IN_MINUTE = 60
MOVING_AVG_LEN = int(SECONDS_IN_MINUTE / SLEEP_TIME)

aqis = deque(maxlen=MOVING_AVG_LEN)
vocss = deque(maxlen=MOVING_AVG_LEN)
co2s = deque(maxlen=MOVING_AVG_LEN)
temps = deque(maxlen=MOVING_AVG_LEN)
hums = deque(maxlen=MOVING_AVG_LEN)
pressures = deque(maxlen=MOVING_AVG_LEN)
i=0
while True:
    temp, pressure, humidity = get_bme_data()
    temps.append(temp)
    pressures.append(pressure)
    hums.append(humidity)
    aqi, vocs, co2, status = None, None, None, None

    if ens is not None:
        try:
            aqi, vocs, co2, status = ens.get_all_data(temperature=temp, humidity=humidity)
            aqis.append(aqi)
            vocss.append(vocs)
            co2s.append(co2)
        except Exception as ex:
            print('cannot get ENS sensor data.')
            print(ex)

        print('Status: {}'.format(status))
        print('Air index: {}/5'.format(int(aqi)))
        print('VOCS: {}ppb'.format(int(vocs)))
        print('CO2: {}ppm'.format(int(co2)))

    print('Temperature: {:.1f}*C'.format(temp))
    print('Humidity: {:.1f}%'.format(humidity))
    print('Pressure: {:.2f}hPa\n'.format(pressure))
    i += 1
    if i == MOVING_AVG_LEN:
        i = 0
        aqi_avg = int(get_avg(aqis))
        vocs_avg = int(get_avg(vocss))
        co2_avg = int(get_avg(co2s))
        temp_avg = round(get_avg(temps), 1)
        humidity_avg = round(get_avg(hums), 1)
        pressure_avg = round(get_avg(pressures), 2)

        logger.append_record({'temp': temp_avg, 'pressure': pressure_avg, 'humidity': humidity_avg,
                              'aqi': aqi_avg, 'vocs': vocs_avg, 'co2': co2_avg})

    sleep(SLEEP_TIME)
