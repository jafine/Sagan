from time import *
from smbus import *
from GenericSensor import *

BIT0	=	1 << 0
BIT1	=	1 << 1
BIT2	=	1 << 2
BIT3	=	1 << 3
BIT4	=	1 << 4
BIT5	=	1 << 5
BIT6	=	1 << 6
BIT7	=	1 << 7

class VEML6070(GenericSensor):
	def __init__(self, pAddr, pLabel):
		readings = \
		[
			Reading("UV", 	"uW/cm^2")
		]
		#Run the inherited constructor, this initialises
                # the i2c bus and provides an interface object
		GenericSensor.__init__(self, pAddr, pLabel, readings)

		#Write the initialisation settings
		IT = 1 <<2
		SD = 0 
		ACK = 0 << 5
		self.mCommand = ACK | SD | IT
		self.write8(self.mCommand)
		sleep(0.25)
		self.readU8(self.mAddr)
		self.readU8(self.mAddr + 1)

	def write8(self, pValue):
		self.mBus.write_byte(self.mAddr, BIT8(pValue))

	def readU8(self, pAddress):
		return BIT8(self.mBus.read_byte(pAddress))

	def ReadRawUV(self):
		LSB = self.readU8(self.mAddr)
		MSB = self.readU8(self.mAddr + 1)
		return (LSB | (MSB << 8))
	def ReadUV(self):
		return float(self.ReadRawUV())*5.0
	
	def Sample(self, pReading):
		#Note, for the LM75B, there is only one reading, therefore
		#Read(0, 2)
		#This will trigger an exeption if reading is incorrect
		self.GetReadingIndex(pReading)

		# Go through the various sensors
		if (pReading == "UV"):
			return self.ReadUV();
		else:
			raise Exception("Invalid reading name.")

#test = VEML6070(0x38, "VEML6070")
#print(test.ToString("UV"))
