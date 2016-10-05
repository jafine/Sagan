import RPi.GPIO as GPIO

class LEDS:
	_LED1 = 27
	_LED2 = 22
	_RED = 25
	_GREEN = 23
	_BLUE = 24
	_ON = False
	_OFF = True

	def __init__(self):
		GPIO.setmode(GPIO.BCM)

		#Check that the mode is set correctly
		self.mode = GPIO.getmode()
		if (self.mode != 11):
			raise Exception("GPIO Not in BCM mode, try run program as superuser (sudo).")

		#Disable warnings, they are annoying and don't mean anything in this case
		GPIO.setwarnings(False)		
		
		#Configure LED1 as output
		GPIO.setup(self._LED1,		GPIO.OUT)

		#Configure LED2 as output
		GPIO.setup(self._LED2,		GPIO.OUT)
		
		#Configure RGB pins as outputs
		GPIO.setup(self._RED,		GPIO.OUT)
		GPIO.setup(self._GREEN,		GPIO.OUT)
		GPIO.setup(self._BLUE,		GPIO.OUT)

		#Set all pins as off
		GPIO.output(self._LED1,		self._OFF)
		GPIO.output(self._LED2,		self._OFF)
		GPIO.output(self._RED,		self._OFF)
		GPIO.output(self._GREEN,	self._OFF)
		GPIO.output(self._BLUE,		self._OFF)

		#Setup LED dictionary
		self.LEDLookup = \
			{
			'LED1':	self._LED1,
			'LED2':	self._LED2,
			'RED':	self._RED,
			'GREEN':self._GREEN,
			'BLUE':	self._BLUE
			}

	def LEDOn(self, pLabel):
		pLabel = pLabel.upper()
		GPIO.output(self.LEDLookup[pLabel], self._ON)

        def LEDOff(self, pLabel):
		pLabel = pLabel.upper()
                GPIO.output(self.LEDLookup[pLabel], self._OFF)
