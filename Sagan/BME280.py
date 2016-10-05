import time

from smbus import *
from GenericSensor import *

BME280_REGISTER_T1 = 0x88  # Trimming parameter registers
BME280_REGISTER_T2 = 0x8A
BME280_REGISTER_T3 = 0x8C

BME280_REGISTER_P1 = 0x8E
BME280_REGISTER_P2 = 0x90
BME280_REGISTER_P3 = 0x92
BME280_REGISTER_P4 = 0x94
BME280_REGISTER_P5 = 0x96
BME280_REGISTER_P6 = 0x98
BME280_REGISTER_P7 = 0x9A
BME280_REGISTER_P8 = 0x9C
BME280_REGISTER_P9 = 0x9E

BME280_REGISTER_H1 = 0xA1
BME280_REGISTER_H2 = 0xE1
BME280_REGISTER_H3 = 0xE3
BME280_REGISTER_H4 = 0xE4
BME280_REGISTER_H5 = 0xE5
BME280_REGISTER_H6 = 0xE6
BME280_REGISTER_H7 = 0xE7

BME280_REGISTER_CHIPID = 0xD0
BME280_REGISTER_VERSION = 0xD1
BME280_REGISTER_SOFTRESET = 0xE0

BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_CONTROL = 0xF4
BME280_REGISTER_CONFIG = 0xF5
BME280_REGISTER_PRESSURE_DATA = 0xF7
BME280_REGISTER_TEMP_DATA = 0xFA
BME280_REGISTER_HUMIDITY_DATA = 0xFD

#Interface class for the LM75B
class BME280(GenericSensor):
	T1 = 0
	T2 = 0
	T3 = 0
	P1 = 0
	P2 = 0
	P3 = 0
	P4 = 0
	P5 = 0
	P6 = 0
	P7 = 0
	P8 = 0
	P9 = 0
	H1 = 0
	H2 = 0
	H3 = 0
	H4 = 0
	H5 = 0
	H6 = 0

        def __init__(self, pAddr, pLabel):
                readings = \
                [
                        Reading("Temperature", 	degree_sign + "K"),
			Reading("Pressure", 	"kPa"),
			Reading("Altitude", 	"m"),
			Reading("Humidity", 	"%")
                ]
                #Run the inherited constructor, this initialises
                # the i2c bus and provides an interface object
                GenericSensor.__init__(self, pAddr, pLabel, readings)
		
		CHIPID = self.readU8(BME280_REGISTER_CHIPID)
		if (CHIPID != 0x60):
			raise Exception("BMP280 chip ID is incorrect! It is " + hex(CHIPID) + " and should be 0x58.")
		self._mode = 3
		
		# Load calibration values.
		self.readCoefficients()
		self.write8(BME280_REGISTER_CONTROL, 0x3F)
		self.t_fine = 0.0

	def write8(self, pRegister, pValue):
		self.mBus.write_byte_data(self.mAddr, pRegister, BIT8(pValue))
	def readU8(self, pRegister):
		return BIT8(self.mBus.read_byte_data(self.mAddr, pRegister))		
	def readS8(self, pRegister):
		return SBIT8(self.readU8(pRegister))	

	def readU16_LE(self, pRegister):
		return BIT16(self.mBus.read_word_data(self.mAddr, pRegister))
	def readU16(self, pRegister):
		result = self.readU16(pRegister)
		result = ((result << 8) & 0xFF00) + (result >> 8)
		return result

	def readS16_LE(self, pRegister):
		return SBIT16(self.readU16_LE(pRegister))
	def readS16(self, pRegister):
		return SBIT16(self.readU16(pRegister))

	def readCoefficients(self):
		#Get the temperature registers
		self.T1 = self.readU16_LE(BME280_REGISTER_T1)
		self.T2 = self.readS16_LE(BME280_REGISTER_T2)
		self.T3 = self.readS16_LE(BME280_REGISTER_T3)
		
		#Get the pressure registers
		self.P1 = self.readU16_LE(BME280_REGISTER_P1)
		self.P2 = self.readS16_LE(BME280_REGISTER_P2)
		self.P3 = self.readS16_LE(BME280_REGISTER_P3)
		self.P4 = self.readS16_LE(BME280_REGISTER_P4)
		self.P5 = self.readS16_LE(BME280_REGISTER_P5)
		self.P6 = self.readS16_LE(BME280_REGISTER_P6)
		self.P7 = self.readS16_LE(BME280_REGISTER_P7)
		self.P8 = self.readS16_LE(BME280_REGISTER_P8)
		self.P9 = self.readS16_LE(BME280_REGISTER_P9)
		
		#Get the humidity registers
		self.H1 = self.readU8(BME280_REGISTER_H1)
		self.H2 = self.readS16_LE(BME280_REGISTER_H2)
		self.H3 = self.readU8(BME280_REGISTER_H3)
		self.H6 = self.readS8(BME280_REGISTER_H7)
		
		h4 = self.readS8(BME280_REGISTER_H4)
		h4 = (h4 << 24) >> 20
		self.H4 = h4 | (self.readU8(BME280_REGISTER_H5) & 0x0F)
		h5 = self.readS8(BME280_REGISTER_H6)
		h5 = (h5 << 24) >> 20
		self.H5 = h5 | (self.readU8(BME280_REGISTER_H5) >> 4 & 0x0F)

	def read_raw_temp(self):
		"""Reads the raw (uncompensated) temperature from the sensor."""
		meas = self._mode
		self.write8(BME280_REGISTER_CONTROL_HUM, meas)
		meas = self._mode << 5 | self._mode << 2 | 1
		self.write8(BME280_REGISTER_CONTROL, meas)
		sleep_time = 0.00125 + 0.0023 * (1 << self._mode)
		sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
		sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
		time.sleep(sleep_time)  
		
		# Wait the required time
		msb = self.readU8(BME280_REGISTER_TEMP_DATA)
		lsb = self.readU8(BME280_REGISTER_TEMP_DATA + 1)
		xlsb = self.readU8(BME280_REGISTER_TEMP_DATA + 2)
		raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
		return raw
	
	def read_raw_pressure(self):
		"""Reads the raw (uncompensated) pressure level from the sensor."""
		"""Assumes that the temperature has already been read """
		"""i.e. that enough delay has been provided"""
		msb = self.readU8(BME280_REGISTER_PRESSURE_DATA)
		lsb = self.readU8(BME280_REGISTER_PRESSURE_DATA + 1)
		xlsb = self.readU8(BME280_REGISTER_PRESSURE_DATA + 2)
		
		raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
		return raw

	def read_raw_humidity(self):
		"""Assumes that the temperature has already been read """
		"""i.e. that enough delay has been provided"""
		meas = self._mode
		self.write8(BME280_REGISTER_CONTROL_HUM, meas)
		meas = self._mode << 5 | self._mode << 2 | 1
		self.write8(BME280_REGISTER_CONTROL, meas)
		msb = self.readU8(BME280_REGISTER_HUMIDITY_DATA)
		lsb = self.readU8(BME280_REGISTER_HUMIDITY_DATA + 1)
		raw = (msb << 8) | lsb
		return raw


	def ReadTemperature(self):
		"""Gets the compensated temperature in degrees celsius."""
		# float in Python is double precision
		UT = float(self.read_raw_temp())
		var1 = (UT / 16384.0 - self.T1 / 1024.0) * float(self.T2)
		var2 = ((UT / 131072.0 - self.T1 / 8192.0) * (UT / 131072.0 - self.T1 / 8192.0)) * float(self.T3)
		self.t_fine = int(var1 + var2)
		temp = (var1 + var2) / 5120.0
		return temp + 273.15

	def ReadPressure(self):
		"""Gets the compensated pressure in Pascals."""
		adc = self.read_raw_pressure()
		var1 = self.t_fine / 2.0 - 64000.0
		var2 = var1 * var1 * self.P6 / 32768.0
		var2 = var2 + var1 * self.P5 * 2.0
		var2 = var2 / 4.0 + self.P4 * 65536.0
		var1 = (self.P3 * var1 * var1 / 524288.0 + self.P2 * var1) / 524288.0
		var1 = (1.0 + var1 / 32768.0) * self.P1
		
		if var1 == 0:
			return 0
		
		p = 1048576.0 - adc
		p = ((p - var2 / 4096.0) * 6250.0) / var1
		var1 = self.P9 * p * p / 2147483648.0
		var2 = p * self.P8 / 32768.0
		p = p + (var1 + var2 + self.P7) / 16.0
		return p / 1000

	def ReadHumidity(self):
		adc = self.read_raw_humidity()
	        # print 'Raw humidity = {0:d}'.format (adc)
	        h = self.t_fine - 76800.0
	        h = (adc - (self.H4 * 64.0 + self.H5 / 16384.8 * h)) * (
	        self.H2 / 65536.0 * (1.0 + self.H6 / 67108864.0 * h * (
	        1.0 + self.H3 / 67108864.0 * h)))
	        h = h * (1.0 - self.H1 * h / 524288.0)
	        if h > 100:
	            h = 100
	        elif h < 0:
	            h = 0
	        return h

	def ReadAltitude(self, SeaLevelHPa = 1013.25):
		pressure = self.ReadPressure()*10 # in Si units for Pascal
		altitude = 44330.0 * (1.0 - pow(pressure / SeaLevelHPa, 0.1903))
		return altitude

        def Sample(self, pReading):                
		output = 0					
		if (pReading is "Temperature"):
			output = self.ReadTemperature()
		elif (pReading is "Pressure"):
			output = self.ReadPressure()
		elif (pReading is "Altitude"):
			output = self.ReadAltitude()
		elif (pReading is "Humidity"):
			output = self.ReadHumidity()
		else:
			raise Exception("Reading " + """ + pReading + """ + " doesn't exist on device.")		
                return output
