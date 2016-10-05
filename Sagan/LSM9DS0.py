from datetime   import datetime
from smbus      import *
from GenericSensor     import *
import time
import math

#Addresses
MAG_ADDRESS		=	0x1D			
ACC_ADDRESS		=	0x1D			
GYR_ADDRESS     	=       0x6B

#LSM9DS0 Gyro Registers	
WHO_AM_I_G		=	0x0F			
CTRL_REG1_G		=	0x20			
CTRL_REG2_G		=	0x21			
CTRL_REG3_G		=	0x22			
CTRL_REG4_G		=	0x23			
CTRL_REG5_G		=	0x24			
REFERENCE_G		=	0x25			
STATUS_REG_G		=	0x27			
OUT_X_L_G		=	0x28			
OUT_X_H_G		=	0x29			
OUT_Y_L_G		=	0x2A			
OUT_Y_H_G		=	0x2B			
OUT_Z_L_G		=	0x2C			
OUT_Z_H_G		=	0x2D			
FIFO_CTRL_REG_G		=	0x2E			
FIFO_SRC_REG_G		=	0x2F			
INT1_CFG_G		=	0x30			
INT1_SRC_G		=	0x31			
INT1_THS_XH_G		=	0x32			
INT1_THS_XL_G		=	0x33			
INT1_THS_YH_G		=	0x34			
INT1_THS_YL_G		=	0x35			
INT1_THS_ZH_G		=	0x36			
INT1_THS_ZL_G		=	0x37			
INT1_DURATION_G		=	0x38			

#LSM9DS0 Accel and Magneto Registers
OUT_TEMP_L_XM		=	0x05			
OUT_TEMP_H_XM		=	0x06			
STATUS_REG_M		=	0x07			
OUT_X_L_M		=	0x08			
OUT_X_H_M		=	0x09			
OUT_Y_L_M		=	0x0A			
OUT_Y_H_M		=	0x0B			
OUT_Z_L_M		=	0x0C			
OUT_Z_H_M		=	0x0D			
WHO_AM_I_XM		=	0x0F			
INT_CTRL_REG_M		=	0x12			
INT_SRC_REG_M		=	0x13			
INT_THS_L_M		=	0x14			
INT_THS_H_M		=	0x15			
OFFSET_X_L_M		=	0x16			
OFFSET_X_H_M		=	0x17			
OFFSET_Y_L_M		=	0x18			
OFFSET_Y_H_M		=	0x19			
OFFSET_Z_L_M		=	0x1A			
OFFSET_Z_H_M		=	0x1B			
REFERENCE_X		=	0x1C			
REFERENCE_Y		=	0x1D			
REFERENCE_Z		=	0x1E			
CTRL_REG0_XM		=	0x1F			
CTRL_REG1_XM		=	0x20			
CTRL_REG2_XM		=	0x21			
CTRL_REG3_XM		=	0x22			
CTRL_REG4_XM		=	0x23			
CTRL_REG5_XM		=	0x24			
CTRL_REG6_XM		=	0x25			
CTRL_REG7_XM		=	0x26			
STATUS_REG_A		=	0x27			
OUT_X_L_A		=	0x28			
OUT_X_H_A		=	0x29			
OUT_Y_L_A		=	0x2A			
OUT_Y_H_A		=	0x2B			
OUT_Z_L_A		=	0x2C			
OUT_Z_H_A		=	0x2D			
FIFO_CTRL_REG		=	0x2E			
FIFO_SRC_REG		=	0x2F			
INT_GEN_1_REG		=	0x30			
INT_GEN_1_SRC		=	0x31			
INT_GEN_1_THS		=	0x32			
INT_GEN_1_DURATION	=	0x33			
INT_GEN_2_REG		=	0x34			
INT_GEN_2_SRC		=	0x35			
INT_GEN_2_THS		=	0x36			
INT_GEN_2_DURATION	=	0x37			
CLICK_CFG		=	0x38			
CLICK_SRC		=	0x39			
CLICK_THS		=	0x3A			
TIME_LIMIT		=	0x3B			
TIME_LATENCY		=	0x3C			
TIME_WINDOW		=	0x3D	

#Interface class for the LSM9DSO
class LSM9DS0(GenericSensor):
	def __init__(self, pAddr, pLabel):
                readings = \
                [
                        Reading("Temperature", 		degree_sign + "K",	Register = OUT_TEMP_L_XM),
			Reading("AccelerationX", 	"m/s^2",		Register = OUT_X_L_A),
			Reading("AccelerationY", 	"m/s^2",		Register = OUT_Y_L_A),
                        Reading("AccelerationZ", 	"m/s^2",		Register = OUT_Z_L_A),
                        Reading("MagnotometerX", 	"B",			Register = OUT_X_L_M),
                        Reading("MagnotometerY", 	"B",			Register = OUT_Y_L_M),
                        Reading("MagnotometerZ", 	"B",			Register = OUT_Z_L_M),
                        Reading("GyroscopeX",	 	"rad/s",		Register = OUT_X_L_G),
                        Reading("GyroscopeY", 		"rad/s",		Register = OUT_Y_L_G),
                        Reading("GyroscopeZ", 		"rad/s",		Register = OUT_Z_L_G)
                ]
                #Run the inherited constructor, this initialises
                # the i2c bus and provides an interface object
                GenericSensor.__init__(self, pAddr, pLabel, readings)
		
		#initialise the accelerometer
		self.Write("Acceleration",CTRL_REG1_XM, 	0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
		self.Write("Acceleration",CTRL_REG2_XM, 	0b00100000) #+/- 16G full scale
		self.Accel_LSB = 0.000732*9.80665

		#initialise the magnetometer
		self.Write("Magnotometer",CTRL_REG5_XM, 	0b11110000) #Temp enable, M data rate = 50Hz
		self.Write("Magnotometer",CTRL_REG6_XM, 	0b01100000) #+/-12gauss
		self.Write("Magnotometer",CTRL_REG7_XM,		0b00000000) #Continuous-conversion mode
		self.Magno_LSB = 0.00048		

		#initialise the gyroscope
		self.Write("Gyroscope", CTRL_REG1_G, 		0b00001111) #Normal power mode, all axes enabled
		self.Write("Gyroscope", CTRL_REG4_G, 		0b00110000) #Continuos update, 2000 dps full scale
		self.Gyro_LSB = 0.070	

        def Sample(self, pReading):
                #This will trigger an exeption if reading is incorrect
                index = self.GetReadingIndex(pReading)

	def Read(self, pDevice, pRegister):
                Gyro = "Gyroscope"
		if (pDevice.find(Gyro) >= 0):
			acc_l = self.mBus.read_byte_data(GYR_ADDRESS, pRegister)
        		acc_h = self.mBus.read_byte_data(GYR_ADDRESS, pRegister + 1)
                else:
			acc_l = self.mBus.read_byte_data(MAG_ADDRESS, pRegister)
	        	acc_h = self.mBus.read_byte_data(MAG_ADDRESS, pRegister + 1)

		return SBIT16(acc_l | acc_h <<8)

	def Write(self, pDevice, pRegister, pValue):
		Gyro = "Gyroscope"
		if (pDevice.find(Gyro) >= 0):
			self.mBus.write_byte_data(GYR_ADDRESS, pRegister, pValue)	
		else:
			self.mBus.write_byte_data(MAG_ADDRESS, pRegister, pValue)

        def Sample(self, pReading):
                #This will trigger an exeption if reading is incorrect
                index = self.GetReadingIndex(pReading)
		Reading = self.mReadings[index]
		Label = Reading.mLabel
		value = self.Read(Label, Reading.mReg)		

		#Convert values to sensable units
		if (Label.find("Acceleration") >= 0):
			value *= self.Accel_LSB
		elif (Label.find("Magnotometer") >= 0):
			value *= self.Magno_LSB
		elif (Label.find("Gyroscope") >= 0):
			value *= self.Gyro_LSB
		else:
			raise Exception("Invalid device parameter")
		
                return value
