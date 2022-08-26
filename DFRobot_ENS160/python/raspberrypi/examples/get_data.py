# -*- coding: utf-8 -*
'''!
  @file  get_temp_press.py
  @brief  Get the sensor data by polling
  @details  Configure the sensor power mode and parameters (for compensating the calibrated temperature and relative humidity in gas measurement)
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license  The MIT License (MIT)
  @author  [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0
  @date  2021-10-28
  @url  https://github.com/DFRobot/DFRobot_ENS160
'''
# from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# from .DFRobot_ENS160 import *
from ..DFRobot_ENS160 import *

class ENS160:
  def __init__(self, temperature=24.00, humidity=60):
    self.temperature = temperature
    self.humidity = humidity
    '''
    # Select communication interface I2C, please comment out SPI interface. And vise versa.
    # I2C : For Fermion version, I2C communication address setting: 
    #         connect SDO pin to GND, I2C address is 0×52 now;
    #         connect SDO pin to VCC(3v3), I2C address is 0x53 now
    # SPI : Set up digital pin according to the on-board pin connected with SPI chip-select pin.
    '''
    self.sensor = DFRobot_ENS160_I2C(i2c_addr=0x53, bus=2)
  # self.sensor = DFRobot_ENS160_SPI(cs=8, bus=0, dev=0, speed=2000000)
    self.is_setup_done = False

  def setup(self):
    while (self.sensor.begin() == False):
      print ('Please check that the device is properly connected')
      time.sleep(3)
    print("sensor begin successfully.")

    '''
      # Configure power mode
      # mode Configurable power mode:
      #   ENS160_SLEEP_MODE: DEEP SLEEP mode (low power standby)
      #   ENS160_IDLE_MODE: IDLE mode (low-power)
      #   ENS160_STANDARD_MODE: STANDARD Gas Sensing Modes
    '''
    self.sensor.set_PWR_mode(ENS160_STANDARD_MODE)

    '''
      # Users write ambient temperature and relative humidity into ENS160 for calibration and compensation of the measured gas data.
      # ambient_temp Compensate the current ambient temperature, float type, unit: C
      # relative_humidity Compensate the current ambient humidity, float type, unit: %rH
    '''
    self.sensor.set_temp_and_hum(ambient_temp=self.temperature, relative_humidity=self.humidity)

  def get_all_data(self, temperature=None, humidity=None):
    if temperature == None:
      temperature = self.temperature
    else:
      self.temperature = temperature
    if humidity == None:
      humidity = self.humidity
    else:
      self.humidity = humidity

    self.sensor.set_temp_and_hum(ambient_temp=temperature, relative_humidity=humidity)

    return self.sensor.get_AQI, self.sensor.get_TVOC_ppb, self.sensor.get_ECO2_ppm

  def loop(self):
    '''
      # Get the sensor operating status
      # Return value: 0-Normal operation, 
      #         1-Warm-Up phase, first 3 minutes after power-on.
      #         2-Initial Start-Up phase, first full hour of operation after initial power-on.Only once in the sensor’s lifetime.
      # note: Note that the status will only be stored in the non-volatile memory after an initial 24h of continuous
      #       operation. If unpowered before conclusion of said period, the ENS160 will resume "Initial Start-up" mode
      #       after re-powering.
    '''
    sensor_status = self.sensor.get_ENS160_status()
    print("Sensor operating status : %u" %sensor_status)

    '''
      # Get the air quality index calculated on the basis of UBA
      # Return value: 1-Excellent, 2-Good, 3-Moderate, 4-Poor, 5-Unhealthy
    '''
    print("Air quality index : %u" %(self.sensor.get_AQI))

    '''
      # Get TVOC concentration
      # Return value range: 0–65000, unit: ppb
    '''
    print("Concentration of total volatile organic compounds : %u ppb" %(self.sensor.get_TVOC_ppb))

    '''
      # Get CO2 equivalent concentration calculated according to the detected data of VOCs and hydrogen (eCO2 – Equivalent CO2)
      # Return value range: 400–65000, unit: ppm
      # Five levels: Excellent(400 - 600), Good(600 - 800), Moderate(800 - 1000), 
      #               Poor(1000 - 1500), Unhealthy(> 1500)
    '''
    print("Carbon dioxide equivalent concentration : %u ppm" %(self.sensor.get_ECO2_ppm))

    print()
    time.sleep(0.5)


if __name__ == "__main__":
  ens160 = ENS160()
  ens160.setup()
  while True:
    ens160.loop()
