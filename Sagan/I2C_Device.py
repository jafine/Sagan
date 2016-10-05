import smbus

class I2C_Device:
	Address = 0x00
	Label = ""
	Device = ""
	Bus = None
	
	#Initialize a single I2C device on the bus provided by the parameters
	def __init__(self, _Address, _Label, _Device):
		#Set general member variables
		self.Address	=	_Address
		self.Label	=	_Label
		self.Device	=	_Device
		#Intialize the bus on (I2C1)
		self.Bus 	=	smbus.SMBus(1)	
	
	#Perform a communciation with the slave device defined above
	def Read(self, _CMD, _ReadCount):
		return self.Bus.read_i2c_block_data(self.Address, _CMD, _ReadCount)
	
	def Write(self, _CMD, _Data):
		self.Bus.write_byte_data(self.Address, _CMD, _Data)
