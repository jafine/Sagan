#!/usr/bin/python
HOME_PATH="/home/pi/control_data_handler/CDH/core"

# import our system path
import sys
sys.path.insert(0, HOME_PATH)

# import our hardware libraries
from Logbook import *
from Sensor import *
from LEDS import *

# import useful system libraries
import signal
import time
import os
from subprocess import call

# import plotting libraries
#import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
#import numpy

#Make a new folder for us
#from datetime import datetime
#folder = datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S")

#if not os.path.exists(folder):
#        os.makedirs(folder)

#os.chdir(folder)

#def mySignalHandler(signal, frame):
#        print "Interrupt signal caught"
#        exit


#signal.signal(signal.SIGINT, mySignalHandler)

