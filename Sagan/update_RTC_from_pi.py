#!/bin/python

from Sensor import *
import time

RTCtime = Sensor("Time")

t = time.gmtime(time.time())
previousTime = RTCtime()

print "RPi UTC current time : ", time.asctime(t)
print "Previous RTC time : ", previousTime

RTC.SetDate(t.tm_year-2000, t.tm_mon, t.tm_mday)
RTC.SetTime(t.tm_hour, t.tm_min, t.tm_sec)

currentTime = RTCtime()

print "RTC current time : ", currentTime
