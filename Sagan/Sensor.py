from Camera import *
from LM75B import *
from BME280 import *
from LSM9DS0 import *
from VEML6070 import *
from APDS_9250 import *
from GenericSensor import *

# ASIMOV MODULE
#from DS3231 import *
#RTC		= DS3231(	0x68,	"DS3231")
#BotTempAddr	= 0x4F
#TopTempAddr	= 0x4B
#InertialAddr	= 0x1D

# SAGAN MODULE
from PCF85263A import *
RTC             = PCF85263A(    0x51,   "PCF85263A")
BotTempAddr	= 0x48
TopTempAddr	= 0x49
InertialAddr	= 0x1E

#One object for each sensor on the device
BotTemp 	= LM75B(BotTempAddr, 	"LM75B")
TopTemp 	= LM75B(TopTempAddr, 	"LM75B")
Inertial 	= LSM9DS0(InertialAddr,	"LSM9DSO")
Barometer 	= BME280(	0x76, 	"BME280")
IR_RGB_ALS	= APDS_9250(	0x52, "APDS-9250")
UV		= VEML6070(	0x38, "VEML6070")
Arducam		= Camera()

#Generic sensor information class, describes the sensor
class SenInfo:
	Sensor = None
	Parameters = None
	
	#Defines the class
	def __init__(self, Sensor, Parameters):
		self.Sensor = Sensor
		self.Parameters = Parameters

#List of avaliable 
Devices = {\
'Top Temperature': 		SenInfo(TopTemp, 	['Temperature']),
'Bottom Temperature':		SenInfo(BotTemp, 	['Temperature']),
'Time': 			SenInfo(RTC, 	 	['All']),
'Acceleration': 		SenInfo(Inertial,	['AccelerationX',	'AccelerationY',	'AccelerationZ']),
'Magnetic Field': 		SenInfo(Inertial,	['MagnotometerX',	'MagnotometerY',	'MagnotometerZ']),
'Rotational Acceleration': 	SenInfo(Inertial, 	['GyroscopeX', 		'GyroscopeY', 		'GyroscopeZ']),
'Humidity': 			SenInfo(Barometer, 	['Humidity']),
'Altitude': 			SenInfo(Barometer,	['Altitude']),
'Pressure': 			SenInfo(Barometer,	['Pressure']),

'Infrared': 			SenInfo(IR_RGB_ALS, 	['IR']),
'Colour': 			SenInfo(IR_RGB_ALS,	['RGB']),
'Ambient Light': 		SenInfo(IR_RGB_ALS,	['Ambient']),

'Ultraviolet': 			SenInfo(UV,		['UV']),
'Image': 			SenInfo(Arducam,	['Photo'])
}


#Sensor interface class
class Sensor:
	Device = None	
	Label = None
	#Initialises a generic device, it links it to the above device
	def __init__(self, pDevice):
		self.Label = pDevice
		self.Device = Devices[pDevice];
	
	#Makes the sensor a functor
	def __call__(self, pFormat = "Short"):
		Sensor = self.Device.Sensor
		Params = self.Device.Parameters
		
		output = []
		for Parameter in Params:
			output.append(Sensor.ToString(Parameter, pFormat))
		
		length = len(output)
		if (length == 3):	
			return Vector(output[0], output[1], output[2])
		elif (length == 1):
			return output[0];
		else:
			raise Exception("It appears a devices parameters have been defined incorrectly")
		return None

	#Returns the sensor data as a string, this can only be value
	def __str__(self):
                Sensor = self.Device.Sensor
                Params = self.Device.Parameters

                output = []
                for Parameter in Params:
                        output.append(Sensor.ToString(Parameter, "Value"))

                length = len(output)
                if (length == 3):
                        return str(Vector(output[0], output[1], output[2]))
                elif (length == 1):
                        return str(output[0]);
                else:
                        raise Exception("It appears a devices parameters have been defined incorrectly")
                return None
    
    def getValue():
        return str(self)

	def getRTC():
		return RTC
