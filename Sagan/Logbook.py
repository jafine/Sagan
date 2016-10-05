from Sensor import Sensor
#from time import *
from Timer import *

import sys

START = \
"""\
<HTML>	
	<HEAD>
	
		<STYLE>
			table.content
			{
				border: 1px #000 solid;
			}
			td.column
			{
				border: 1px #000 solid;
			}
			td.row
			{
				border: 1px #000 solid;
			}
			th.header
			{
				border: 1px #000 solid;
			}
		</STYLE>
	
	</HEAD>
	<BODY>
		<TABLE class = "content">
"""

END = \
"""\
		</TABLE>	
	</BODY>
</HTML>
"""

TABLEHEADER = \
"""\
				<th class = "header">
					${CONTENT}
				</th>
"""


TABLEROW = \
"""\
			<tr class = "row">
${CONTENT}
			</tr>
"""

TABLECOLUMN = \
"""\
				<td class = "column">
					${CONTENT}
				</td>
"""

class TableColumn:
	Heading = None
	NewData = False
	Format = "Short"
	Data = None
	
	def __init__(self, pHeading, pFormat):
		self.Heading = pHeading
		self.Format = pFormat

	
	def Update(self, pData = None):
		if (pData != None):
			self.NewData = True			
		self.Data = pData

class Logbook:
	File = None
	#DataFile = None
	Logging = False
	Columns = []
	Filename = None
	
	def __init__(self, Filename):
		self.Columns = []
		self.Logging = False
		if(Filename == None):
			raise Exception("Filename cannot be None.")
		if(len(Filename)==0):
			raise Exception("Filname cannot have zero length.")		
		self.Filename = Filename

	def AddColumn(self, Heading, Format = "Short"):
		if (self.Logging):
			raise Exception("Cannot add columns after you have startted logging data.")
		for Item in self.Columns:
			if (Heading is Item.Heading):
				raise Exception("The column you added (" + Heading + ") already exists, use another name.")
		self.Columns.append(TableColumn(Heading, Format))

	def Start(self):
		self.File = open(self.Filename + '.html', 'w')
		#self.DataFile = open(self.Filename + '.dat', 'w')
		self.File.write(START)
		#Write the heading labels
		output = ""
		#dataOut = ""
		for Item in self.Columns:
			output += TABLEHEADER.replace("${CONTENT}", Item.Heading)
			#dataOut += Item.Heading + '\t'

		output = TABLEROW.replace("${CONTENT}", output)
		#dataOut += '\n'

		self.File.write(output);
		#self.DataFile.write(dataOut);
		
	def NewData(self, Sensor):
		HeadingFound = False
		self.Logging = True
		for Item in self.Columns:
			if (Item.Heading is Sensor.Label):
				HeadingFound = True
				Item.Update(str(Sensor))
		if(not HeadingFound):
			raise Exception("The logbook heading doesn't yet exist, add it as a column before recording new data.")

	def NextRow(self):
		if (len(self.Columns) == 0):
			raise Exception("Cannot go to next row when there are no columns to begin with, add some before calling this.")
		output = ""
		#dataOut = ""
		for Item in self.Columns:
			if (Item.NewData):
				Data = str(Item.Data)
				output += TABLECOLUMN.replace("${CONTENT}", Data)
				#dataOut += Item.Data + '\t'
				Item.NewData = False
			else:
				output += TABLECOLUMN.replace("${CONTENT}", "")
		output = TABLEROW.replace("${CONTENT}", output)
		#dataOut += '\n'
		self.File.write(output)
		#self.DataFile.write(dataOut)

	def Finish(self):
		self.File.write(END)
		self.File.close()
		#self.DataFile.close()


#Setup sensors used for logging
"""
clock	= Sensor("Time")
toptemp = Sensor("Top Temperature")
bottemp	= Sensor("Bottom Temperature")
accero  = Sensor("Acceleration")
magnot  = Sensor("Magnetic Field")
altdeo  = Sensor("Altitude")
gryocp  = Sensor("Rotational Acceleration")
humide  = Sensor("Humidity")
presur  = Sensor("Pressure")
rgb	= Sensor("Colour")
ir	= Sensor("Infrared")
amb	= Sensor("Ambient Light")
uv	= Sensor("Ultraviolet")
cam	= Sensor("Image")

#Setup your logbook
MyLogbook = Logbook("logbook2")

#Setups your logbook columns
MyLogbook.AddColumn("Time")
MyLogbook.AddColumn("Top Temperature")
MyLogbook.AddColumn("Bottom Temperature")
MyLogbook.AddColumn("Humidity")
MyLogbook.AddColumn("Pressure")
MyLogbook.AddColumn("Magnetic Field")
MyLogbook.AddColumn("Rotational Acceleration")
MyLogbook.AddColumn("Acceleration")
MyLogbook.AddColumn("Altitude")
MyLogbook.AddColumn("Colour")
MyLogbook.AddColumn("Infrared")
MyLogbook.AddColumn("Ambient Light")
MyLogbook.AddColumn("Ultraviolet")
MyLogbook.AddColumn("Image")

#Start the logbook
MyLogbook.Start()

def Function():
	MyLogbook.NewData(clock)
	MyLogbook.NewData(toptemp)
	MyLogbook.NewData(bottemp)
	MyLogbook.NewData(humide)
	MyLogbook.NewData(presur)
	MyLogbook.NewData(magnot)
	MyLogbook.NewData(gryocp)
	MyLogbook.NewData(accero)
	MyLogbook.NewData(altdeo)

	MyLogbook.NewData(rgb)
	MyLogbook.NewData(ir)
	MyLogbook.NewData(amb)
	MyLogbook.NewData(uv)
	MyLogbook.NewData(cam)
	MyLogbook.NextRow()
	
#Begin Logging
SecondTimer = Timer(5, Function)
SecondTimer(5)

#Finish Logbook
MyLogbook.Finish()
"""
