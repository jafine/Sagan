from smbus import *
from GenericSensor import *
import os

IMGHTML = \
"""
<img class = "CameraImage" src="${SOURCE}"\>
"""

#Interface class for the LM75B
class Camera(GenericSensor):
	index = 0
	def __init__(self, pAddr = 0x01, pLabel = "Camera"):
		readings = \
		[
			Reading("Photo", " ")
		]

		self.index = 0			
		#Run the inherited constructor, this initialises
		# the i2c bus and provides an interface object
		GenericSensor.__init__(self, 0x01, pLabel, readings)

	def Sample(self, pReading = "Photo"):
		#Note, for the LM75B, there is only one reading, therefore
		#Read(0, 2)
		#This will trigger an exeption if reading is incorrect
		os.system("sudo /home/pi/control_data_handler/CDH/core/Arducam/ov2640_capture -c " + str(self.index) +".jpg 800x600")
		#os.system("sudo /home/pi/control_data_handler/CDH/core/Arducam/ov2640_digital_camera -f=" + str(self.index) + ".jpg")

		strt = str(self.index) +".jpg"
		self.index += 1;
		return IMGHTML.replace("${SOURCE}", strt)
