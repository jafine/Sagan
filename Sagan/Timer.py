#Timer class is an abstration of the python threading library
import threading
from time import  *

class Timer:
	def __init__(self, Interval, Function, Args = []):
		if (Interval == 0):
			raise Exception("You cannot run a function every 0 seconds, make the interval > 0.")
		
		self.mArgs 	= Args
		self.mInterval 	= Interval
		self.mFunction 	= Function
		self.mThread 	= threading.Timer(Interval, self.Delay)
		self.mRun 	= False	

	def Delay(self):
		self.mRun = True

	def Fctn(self):		
		if (self.mCount > 0):
			if (len(self.mArgs)):
				self.mFunction(self.mArgs)
			else:
				self.mFunction()
		else:
			return True
		self.mCount -= 1
		return False	

	def __call__(self, Count = 0):
		self.mCount = Count
		#
		self.mThread = threading.Timer(self.mInterval, self.Delay)
		self.mThread.start()
		while (True):
			self.mRun = False
			
			while(self.mRun == False):
				sleep(0.001)
		
			self.mThread.cancel()		
			self.mThread = threading.Timer(self.mInterval, self.Delay)
			self.mThread.start()				
			if(self.Fctn()):
				return
			

"""
def Test():
	print("testme")

Bob = Timer(1, Test)
Bob(5)
"""

