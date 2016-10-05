from datetime 	import datetime
from smbus 	import *
from GenericSensor 	import *
import time

def _bcd_to_int(bcd):
	#Decode a 2x4bit BCD to a integer.
	out = 0
	for d in (bcd >> 4, bcd):
		for p in (1, 2, 4 ,8):
			if d & 1:
				out += p
			d >>= 1
		out *= 10
	return out / 10

def _int_to_bcd(n):
	#Encode a one or two digits number to the BCD.
	bcd = 0
	for i in (n // 10, n % 10):
		for p in (8, 4, 2, 1):
			if i >= p:
				bcd += 1
				i -= p
			bcd <<= 1
	return bcd >> 1
"""  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- 39 -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- 4b -- -- -- 4f
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --"""
#Interface class for the LM75B
class PCF85263A(GenericSensor):
	#Returns the day of the week as a string
	def GetDay(self, pDay):
		return {
			1:"Monday",
			2:"Tuesday",
			3:"Wednesday",
			4:"Thursday",
			5:"Friday",
			6:"Saturday",
			7:"Sunday"
		}[pDay]

	#Write a single byte of data
	def WriteData(self, pReg, pData=0x00):
		self.mBus.write_byte_data(self.mAddr, pReg, pData)
	
	#Reads a single byte of data
	def ReadData(self, pData):
		return (self.mBus.read_byte_data(self.mAddr, pData))

        def __init__(self, pAddr, pLabel = "PCF85263A", pCentury = 21):
                readings = \
                [
			Reading("Hundredths",	"centi",	Register = 0x00, Min = 0, Max = 99),
                        Reading("Seconds", 	"sec",		Register = 0x01, Min = 0, Max = 59),
			Reading("Minutes", 	"min",		Register = 0x02, Min = 0, Max = 59),
			Reading("Hours", 	"hours",	Register = 0x03, Min = 0, Max = 23),
			Reading("Day", 		" ",		Register = 0x04, Min = 1, Max = 31),
			Reading("Date", 	" ",		Register = 0xFF, Min = 0, Max = 0),
			Reading("Month", 	"months",	Register = 0x06, Min = 1, Max = 12),
			Reading("Year", 	" ",		Register = 0x07, Min = 0, Max = 99),
			Reading("Time", 	" ", 		Register = 0xFF, Min = 0, Max = 0),
			Reading("All", 		" ", 		Register = 0xFF, Min = 0, Max = 0)
                ]
                #Run the inherited constructor, this initialises
                # the i2c bus and provides an interface object
                GenericSensor.__init__(self, pAddr, pLabel, readings)
		self.mCentury = (pCentury-1) * 100
		self.WriteData(0x28, 0x80)

	def SetTime(self, Hours, Minutes, Seconds):
		self.Write("Hours", 	Hours)
		self.Write("Minutes", 	Minutes)
		self.Write("Seconds", 	Seconds)

	def SetDate(self, Year, Month, Day):
		self.Write("Year",    	Year)
                self.Write("Month",     Month)
                self.Write("Day",      	Day)

	def Write(self, pReading, pValue=0):
		index   = 	self.GetReadingIndex(pReading)
		Reading = 	self.mReadings[index]
		
		#Checks that the data is inside the registers range
		if(not Reading.InRange(pValue)):
			raise Exception("Trying to write invalid data to register:\n\r\
					\tData="+str(pValue)+\
					"\tTo="+str(pReading))
		#Convert data to BCD
		Value = _int_to_bcd(pValue)
		
		#Write data to device
		self.WriteData(Reading.mReg, Value)

        def Sample(self, pReading):
                if (pReading is "All"):
			dd	=	self.ToString(pFormat = "Value", pReading = "Day").zfill(2)
			mm	=	self.ToString(pFormat = "Value", pReading = "Month").zfill(2)
			yyyy	=	self.ToString(pFormat = "Value", pReading = "Year").zfill(4)
			h	=	self.ToString(pFormat = "Value", pReading = "Hours")
			m	=	self.ToString(pFormat = "Value", pReading = "Minutes").zfill(2)
			s	=	self.ToString(pFormat = "Value", pReading = "Seconds").zfill(2)
			cs	=	self.ToString(pFormat = "Value", pReading = "Hundredths").zfill(2)
			Value 	=	yyyy + "/" +  mm + "/" + dd + " "  + h + ":"  + m + ":" + s + "." + cs
		elif (pReading is "Time"):
                        h       =       self.ToString(pFormat = "Value", pReading = "Hours")
                        m       =       self.ToString(pFormat = "Value", pReading = "Minutes").zfill(2)
                        s       =       self.ToString(pFormat = "Value", pReading = "Seconds").zfill(2)
			Value   =       h + ":"  + m + ":" + s
		elif (pReading is "Date"):
			dd      =       self.ToString(pFormat = "Value", pReading = "Day").zfill(2)
                        mm      =       self.ToString(pFormat = "Value", pReading = "Month").zfill(2)
                        yyyy    =       self.ToString(pFormat = "Value", pReading = "Year").zfill(4)
                        Value   =       dd + "/" + mm + "/" + yyyy
		else:
			#Note, for the LM75B, there is only one reading, therefore
                	#Read(0, 2)
			index 	= 	self.GetReadingIndex(pReading)
			Reading = 	self.mReadings[index]
			Data 	= 	self.ReadData(Reading.mReg)
			if (pReading != "Year" and pReading != "Hundredths"):
				Data = Data & 0x7F
			#elif (pReading == "Hundredths"):
			#	print "Hundredths binary: " + "{0:b}".format(Data)
			
			Value	=	_bcd_to_int(Data)
	
			if (pReading == "Year"):
				Value += self.mCentury
		return Value
