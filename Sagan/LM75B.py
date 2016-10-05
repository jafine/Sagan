from smbus import *
from GenericSensor import *

#Interface class for the LM75B
class LM75B(GenericSensor):
	def __init__(self, pAddr, pLabel = "LM75B"):
		readings = \
		[
			Reading("Temperature", degree_sign + "K")
		]			
		#Run the inherited constructor, this initialises
		# the i2c bus and provides an interface object
		GenericSensor.__init__(self, pAddr, pLabel, readings)

	def Sample(self, pReading = "Temperature"):
		#Note, for the LM75B, there is only one reading, therefore
		#Read(0, 2)
		#This will trigger an exeption if reading is incorrect
		self.GetReadingIndex(pReading)
		
		#Get the temperature reading and convert it to the correct
		temp 	=  	self.mBus.read_i2c_block_data(self.mAddr, 0, 2)
		tout	=	float(Signed(temp[0],8)) + float(temp[1])/256.0 + 273.15
		return tout
