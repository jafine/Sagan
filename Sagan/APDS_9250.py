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

MAIN_CTRL 		=	0x00
LS_MEAS_RATE		=	0x04
LS_GAIN			=	0x05
PART_ID			=  	0x06
MAIN_STATUS		=	0x07
LS_DATA_IR_0		=	0x0A
LS_DATA_IR_1		=	0x0B
LS_DATA_IR_2		=	0x0C
LS_DATA_GREEN_0		=	0x0D
LS_DATA_GREEN_1		=	0x0E
LS_DATA_GREEN_2		=	0x0F
LS_DATA_BLUE_0		=	0x10
LS_DATA_BLUE_1		=	0x11
LS_DATA_BLUE_2		=	0x12
LS_DATA_RED_0		=	0x13
LS_DATA_RED_1		=	0x14
LS_DATA_RED_2		=	0x15
INT_CFG			=	0x19
INT_PERSISTENCE		=	0x1A
LS_THRES_UP_0		=	0x21
LS_THRES_UP_1		=	0x22
LS_THRES_UP_2		=	0x23
LS_THRES_LOW_0		=	0x24
LS_THRES_LOW_1		=	0x25
LS_THRES_LOW_2		=	0x26
LS_THRES_VAR		=	0x27

class APDS_9250(GenericSensor):
	mConfig = 0x00

	def __init__(self, pAddr, pLabel):
		readings = \
		[
			Reading("IR", 		"?"),
			Reading("RGB", 		"%"),
			Reading("Ambient", 	"lux")
		]
		#Run the inherited constructor, this initialises
                # the i2c bus and provides an interface object
		GenericSensor.__init__(self, pAddr, pLabel, readings)
		
		#Verify the CHIP ID
		CHIPID = self.readU8(PART_ID)
		if (CHIPID & 0xF0 != 0xB0):
			raise Exception("APDS-9250 chip ID is incorrect! It is " + hex(CHIPID) + " and should be 0x58.")

		#initailise the device with the following settings
		# IR measurement enabled
		# LUX measurement enabled
		# RGB measureuemnt enabled
		# 10Hz measurements
		# 18 bits
		# ALS Active, IR Active
		# Gain 3
		# Triggers a reset, ensures default values are loaded
		self.write8(MAIN_CTRL, 0x10)

		#Enable ALS, IR and compensation channels activated
		#	0 = ALS, IR and compensation channels activated
		#	1 = All RGB+IR + compensation channels activated
		self.mConfig &= ~BIT2
		self.mConfig |= BIT1	#Enable the light sensor or RGB
		self.write8(MAIN_CTRL, self.mConfig)

		#Read main status register
		LSDATA = 0
		while(LSDATA == 0):
			# Delay 200ms
			STATUS = self.readU8(MAIN_STATUS)
			LSDATA = (STATUS & BIT3) >> 3
			
		INTERR = (STATUS & BIT4) >> 4
		PWRSTA = (STATUS & BIT5) >> 5

		#Configure the measurement rate
		self.mRate = 0x00

		#0x00 20 bit 400ms
		#0x01 19 bit 200ms
		#0x02 18 bit 100ms (default)
		#0x03 17 bit 50ms
		#0x04 16 bit 25ms
		#0x05 13 bit 3.125ms
		self.mRate |= 0x02 << 4 #CHANGE RATE HERE
		self.mRate |= 0x02 << 4 #CHANGE RESOLUTION HERE
		self.write8(MAIN_CTRL, self.mRate)

		#Configure the gain
		self.mGain = 0x00
		self.mGain |= 0x01
		self.write8(MAIN_CTRL, self.mGain)

		#Configure the interrupt register
		self.mIntCfg = 0x00
		self.write8(INT_CFG, self.mIntCfg)

	def write8(self, pRegister, pValue):
		sleep(0.01)
		self.mBus.write_byte_data(self.mAddr, pRegister, BIT8(pValue))
		sleep(0.01)

	def readU8(self, pRegister):
		sleep(0.01)
		return BIT8(self.mBus.read_byte_data(self.mAddr, pRegister))
		sleep(0.01)

	def SetModeRGB(self):
		#Enable ALS, IR and compensation channels activated
		#	0 = ALS, IR and compensation channels activated
		#	1 = All RGB+IR + compensation channels activated
		self.mConfig |= BIT2	#All RGB+IR + compensation channels activated
		self.mConfig |= BIT1	#Enable the light sensor or RGB
		self.write8(MAIN_CTRL, self.mConfig)
		sleep(0.05)

	def SetModeALS(self):
		#Enable ALS, IR and compensation channels activated
		#	0 = ALS, IR and compensation channels activated
		#	1 = All RGB+IR + compensation channels activated
		self.mConfig &= ~BIT2	#ALS, IR and compensation channels activated
		self.mConfig |= BIT1	#Enable the light sensor or RGB
		self.write8(MAIN_CTRL, self.mConfig)
		sleep(0.05)

	def ReadRawIR(self):
		#LS_DATA_IR_0	=	0x0A
		#LS_DATA_IR_1	=	0x0B
		#LS_DATA_IR_2	=	0x0C
		B0 = (self.readU8(LS_DATA_IR_0) << 0)
		B1 = (self.readU8(LS_DATA_IR_1) << 8)
		B2 = (self.readU8(LS_DATA_IR_2) << 16)
		return (B0 | B1 | B2)
	def ReadIR(self):
		return self.ReadRawIR()

	def ReadRawALS(self):
		#LS_DATA_GREEN_0=	0x0D
		#LS_DATA_GREEN_1=	0x0E
		#LS_DATA_GREEN_2=	0x0F
		self.SetModeALS();

		B0 = (self.readU8(LS_DATA_GREEN_0) << 0)
		B1 = (self.readU8(LS_DATA_GREEN_1) << 8)
		B2 = (self.readU8(LS_DATA_GREEN_2) << 16)
		return (B0 | B1 | B2)
	def ReadALS(self):
		return self.ReadRawALS()

	def ReadRawColour(self):
		#LS_DATA_GREEN_0=	0x0D
		#LS_DATA_GREEN_1=	0x0E
		#LS_DATA_GREEN_2=	0x0F
		self.SetModeRGB();
		
		#Get the red components
		R0 = self.readU8(LS_DATA_RED_0) << 0
		R1 = self.readU8(LS_DATA_RED_1) << 8
		R2 = self.readU8(LS_DATA_RED_2) << 16
		RED = float(R0 | R1 | R2)

		#Get the green components
		G0 = self.readU8(LS_DATA_GREEN_0) << 0
		G1 = self.readU8(LS_DATA_GREEN_1) << 8
		G2 = self.readU8(LS_DATA_GREEN_2) << 16
		GREEN = float(G0 | G1 | G2)

		#Get the blue components
		B0 = self.readU8(LS_DATA_BLUE_0) << 0
		B1 = self.readU8(LS_DATA_BLUE_1) << 8	
		B2 = self.readU8(LS_DATA_BLUE_2) << 16
		BLUE = float(B0 | B1 | B2)

		return Vector(RED, GREEN, BLUE, "RGB")
		
	def ReadColour(self):
		RAW = self.ReadRawColour()
		R = RAW.X
		G = RAW.Y
		B = RAW.Z
		TOTAL = R+G+B
		return Vector(R/TOTAL*100, G/TOTAL*100, B/TOTAL*100, "RGB")

	def Sample(self, pReading):
		#Note, for the LM75B, there is only one reading, therefore
		#Read(0, 2)
		#This will trigger an exeption if reading is incorrect
		self.GetReadingIndex(pReading)

		# Go through the various sensors
		if (pReading == "IR"):
			return self.ReadIR();
		elif (pReading == "RGB"):
			return self.ReadColour();
		elif (pReading == "Ambient"):
			return self.ReadALS();
		else:
			raise Exception("Invalid reading name.")

#test = APDS_9250(0x52, "APDS-9250")
#print(test.ToString("IR"))
#print(test.ToString("RGB"))
#print(test.ToString("Ambient"))