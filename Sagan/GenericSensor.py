# -*- coding: utf-8 -*-
import smbus
import sys
global degree_sign
degree_sign= u'\N{DEGREE SIGN}'

def Signed(number, bitLength):
        basetop = 1<<bitLength
        base = (basetop/2) - 1
        if (number > base):
                number -= basetop
        return number

def BIT32(pValue):
        return (pValue & 0xFFFFFFFF)
def SBIT32(pValue):
        pValue &= 0xFFFFFFFF
        return Signed(pValue, 32)

def BIT16(pValue):
        return (pValue & 0xFFFF)
def SBIT16(pValue):
        pValue &= 0xFFFF
        return Signed(pValue, 16)

def BIT8(pValue):
        return (pValue & 0xFF)
def SBIT8(pValue):
        pValue &= 0xFF
        return Signed(pValue, 8)

def clear():
	sys.stderr.write("\x1b[2J\x1b[H")	
	
#The class that is used for the output of the above sensors
class Vector:
	X = 0.0;
	Y = 0.0;
	Z = 0.0;
	
	#Standard 3D vector
	def __init__(self, pX, pY, pZ, pLabels = "XYZ"):
		self.X = pX;
		self.Y = pY;
		self.Z = pZ;
		self.mLabels = pLabels;
		
		if (len(self.mLabels) != 3):
			raise Exception("There must be a label for all axis (eg. \"XYZ\").")
	
	def __str__(self):
		output = ""
		output += self.mLabels[0] + "=" +  str(self.X) + ", "
		output += self.mLabels[1] + "=" + str(self.Y) + ", "
		output += self.mLabels[2] + "=" + str(self.Z)
		return output	

#Used to represent an indivudual reading from one particular sensor
#on a module, modules such as barometers or accelerometers typically have
#multiple sensors (temperature, pressure or acceleration of X, Y and Z)
class Reading:
	mReg		=	0x00		#The register on the sensor
	mLabel 		=	"Unnamed"	#The label of the sensor reading
	mUnits		=	"null"		#The units for the sensor readings
					# (eg, "m/s^2")
	#####################################################################
	#Intiialises a reading class object
	def __init__(self, Label, Units, Max = 0, Min = 0, Register = 0):
		if (len(Label) == 0):
			raise Exception("Cannot have blank sensor label.")
		if (len(Units) == 0):
			raise Exception("Sensor reading cannot be unitless.")
		#Intialises the class members		
		self.mLabel	= 	Label
		self.mUnits 	=	Units
		self.mReg 	=	Register
		self.mMax	=	Max
		self.mMin	=	Min
	
	#Checks that a value to be written is in range
	def InRange(self, pValue):
		if (pValue > self.mMax):
			return False
		if (pValue < self.mMin):
			return False
		return True

#############################################################################
#	Generic Sensor Class
#############################################################################
class GenericSensor:
	mAddr		=	0x00		#Represents sensor I2C address
	mLabel		=	"Unnamed"	#Represents sensor name (eg, "LM75B")
	mBus		=	None		#Represents the I2C bus interface
	mReadings	=	[]

	#####################################################################
	#Initialises the sensor in a general fashion, all classes should call
	#this function before continuing with their initiialisation
	def __init__(self, pAddr, pLabel, pReadings):
		if (pAddr == 0):
			raise Exception("I2C address cannot be zero.")
		if (len(pLabel) == 0):
			raise Exception("Sensor cannot have no name.")
		if (len(pReadings) == 0):
			raise Exception("Sensor cannot have no readings.")
		
		#Initialise member variables
		self.mAddr 	= 	pAddr
		self.mLabel 	= 	pLabel	
		self.mReadings	=	pReadings
		
		#On ASIMOV, I2C is always I2C_1
		self.mBus 	= 	smbus.SMBus(1)	

	#Returns the index inside the readings list
	def GetReadingIndex(self, pReading):
		index = 0
		for item in self.mReadings:
			if (item.mLabel is pReading):
				return index
			index += 1	
		#Should never reach this point
		raise Exception("Reading doesn't exist, use one that does!\r\n ->"+str(pReading))
	
	#####################################################################
	#Gets a single sensor reading
	#	returns data defined by parameters:
	#	pData: 	Defines which value to read
	#		and return.
	#		All is always an option	
	def Sample(self, pReading = "null"):
		return 0
	
        #####################################################################
        #Performs a single write operation to the sensor
	#	pReading:	Defines the location to write to
        #       pValue:  	Defines which value to write
        def Write(self, pReading, pValue=0):
                return 0	

        #####################################################################
        #Converts a sensor reading to a formatted string
        #       pReading:  	The data to output in a string
        #      	pFormat:	The format of the outputted data
	def ToString(self, pReading = "null", pFormat="Full"):
		output = ""
		index = self.GetReadingIndex(pReading)
		if (pFormat == "Value"):
			#This creates a string that is:
			# 	value
			output += str(self.Sample(pReading))
		elif (pFormat == "Short"):
			#This creates a string that is:
			# 	value +  units
			output += str(self.Sample(pReading))
			reading = self.mReadings[index]
			output += " " + reading.mUnits
		elif (pFormat == "Long"):
			#This creates a string that is:
			# 	Reading + "=" + value + units
			reading = self.mReadings[index]
			output += reading.mLabel
			output += " = "
			output += str(self.Sample(pReading))
			output += " " + reading.mUnits
		elif (pFormat == "Full"):
			#This creates a string that is:
			# Sensor
			# 	Reading + "=" + value + units
			reading = self.mReadings[index]
			output += self.mLabel + ": "	
			output += reading.mLabel
                        output += " = "
                        output += str(self.Sample(pReading))
                        output += " " + reading.mUnits
		else:
			raise Exception("Incorrect format specifier, only supports:\
					\r\n\tShort, Long, Value, Full")
		return output
