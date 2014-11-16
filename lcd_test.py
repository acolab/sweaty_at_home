#!/usr/bin/python
 
############################
# Imports                  #
############################
import threading
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import urllib2
 
############################
# Class de controle du LCD #
############################
class HD44780(threading.Thread):
	######################
	# Variable Shared    #
	######################
	_PULSE = 0.00005
	_DELAY = 0.00005
 
	######################
	# Constructeur       #
	######################
	def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18], lcd_width=16):
		self.message = ""
		self.currentmessage = "ACoLab - Hackathlon"
		self.stop = False
		self.lcd_width = lcd_width
		self.pin_rs = pin_rs
		self.pin_e = pin_e
		self.pins_db = pins_db
		GPIO.setmode(GPIO.BCM) 				# Use BCM GPIO numbers
		GPIO.setup(self.pin_e, GPIO.OUT)
		GPIO.setup(self.pin_rs, GPIO.OUT)
		for pin in self.pins_db:
			GPIO.setup(pin, GPIO.OUT)
 
		self.Clear()
		threading.Thread.__init__(self)
 
	######################
	# Demarrage du Thread# 
	######################
	def run(self):
		while self.stop == False:
			if self.message != self.currentmessage:
				self.currentmessage = self.message
				self.LcdMessage()
			sleep(1)
 
	######################
	# Arret du Thread    # 
	######################	
	def Stop(self):
		self.stop = True
 
	######################
	# Initialisation LCD # 
	######################
	def Clear(self):
		""" Blank / Reset LCD """
		self.LcdByte(0x33, False) # $33 8-bit mode
		self.LcdByte(0x32, False) # $32 8-bit mode
		self.LcdByte(0x28, False) # $28 8-bit mode
		self.LcdByte(0x0C, False) # $0C 8-bit mode
		self.LcdByte(0x06, False) # $06 8-bit mode
		self.LcdByte(0x01, False) # $01 8-bit mode
 
	######################
	#Execution sur le LCD# 
	######################
	def LcdByte(self, bits, mode):
		""" Send byte to data pins """
		# bits = data
		# mode = True  for character
		#        False for command
 
		GPIO.output(self.pin_rs, mode) # RS
 
		# High bits
		for pin in self.pins_db:
			GPIO.output(pin, False)
		if bits&0x10==0x10:
			GPIO.output(self.pins_db[0], True)
		if bits&0x20==0x20:
			GPIO.output(self.pins_db[1], True)
		if bits&0x40==0x40:
			GPIO.output(self.pins_db[2], True)
		if bits&0x80==0x80:
			GPIO.output(self.pins_db[3], True)
 
		# Toggle 'Enable' pin
		sleep(HD44780._DELAY)    
		GPIO.output(self.pin_e, True)  
		sleep(HD44780._PULSE)
		GPIO.output(self.pin_e, False)  
		sleep(HD44780._DELAY)      
 
		# Low bits
		for pin in self.pins_db:
			GPIO.output(pin, False)
		if bits&0x01==0x01:
			GPIO.output(self.pins_db[0], True)
		if bits&0x02==0x02:
			GPIO.output(self.pins_db[1], True)
		if bits&0x04==0x04:
			GPIO.output(self.pins_db[2], True)
		if bits&0x08==0x08:
			GPIO.output(self.pins_db[3], True)
 
		# Toggle 'Enable' pin
		sleep(HD44780._DELAY)    
		GPIO.output(self.pin_e, True)  
		sleep(HD44780._PULSE)
		GPIO.output(self.pin_e, False)  
		sleep(HD44780._DELAY) 	
 
	######################
	#Affichage sur le LCD# 
	######################	
	def LcdMessage(self):
		""" Send string to LCD. Newline wraps to second line"""
		self.Clear()
		text = self.currentmessage
		self.LcdByte(0x80, False)
		for c in text:
			if c == '\n':
				self.LcdByte(0xC0, False) # next line
			else:
				self.LcdByte(ord(c),True)
 
	######################
	#Definir le message  # 
	######################
	def LcdSetMessage(self, text):
		self.message = text.ljust(self.lcd_width," ")
 
################################
# Class Informations Systeme   #
################################
class SysInfo(threading.Thread):
	######################
	# Constructeur       #
	######################
	def __init__(self):
		self.count = 0
		self.lcd = HD44780()
		self.stop = False
		threading.Thread.__init__(self)
 
	######################
	# Demarrage du Thread# 
	######################
	def run(self):
		self.lcd.start()
		while self.stop == False:
			if True:
				try:
					msg = urllib2.urlopen("http://localhost:5000/lcd").read()
					self.lcd.LcdSetMessage(msg)
				except:
					self.lcd.LcdSetMessage("Erreur")
			elif self.count == 0: #UPTIME
				self.lcd.LcdSetMessage("Uptime:\n"+self.SysUptime())
			elif self.count == 1: #LOAD
				self.lcd.LcdSetMessage("Load:\n"+self.SysLoadAvg())
			elif self.count == 2: #CPU
				self.lcd.LcdSetMessage("Cpu:\n"+self.SysCpu())
			elif self.count == 3: #MEMORY
				self.lcd.LcdSetMessage("Memory:\n"+self.SysMemory())
			elif self.count == 4: #DRIVE
				self.lcd.LcdSetMessage("Disk Root:\n"+self.SysDisk())
			else:
				self.lcd.LcdSetMessage("Vive l'Auvergne Libre \n ACoLab - Hackathon")
			self.count += 1
			if self.count == 6:
				self.count = 0
			sleep(2)
 
	######################
	# Arret du Thread    # 
	######################
	def Stop(self):
		self.lcd.Stop()
		self.stop = True	
 
	######################
	# Memory             # 
	######################		
	def SysMemory(self):
		try:
			command="free -h"
			process=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			stdout_list=process.communicate()[0].split('\n')
			for line in stdout_list:
			  data=line.split()
			  try:
				  if data[0]=="Mem:":
					  total=str(data[1])
					  used=str(data[2])
					  free=str(data[3])
			  except IndexError:
				  continue	
		except:
			return "Error"
		return str(used)+ " / "+str(total)
 
	######################
	# Disk              # 
	######################		
	def SysDisk(self):
		try:
			command="df -H /"
			process=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			stdout_list=process.communicate()[0].split('\n')
			for line in stdout_list:
			  data=line.split()
			  try:
				  if data[len(data)-1]=="/":
					  total=str(data[1])
					  used=str(data[2])
			  except IndexError:
				  continue	
		except Exception, e:
			print e
			return "Error"
		return str(used)+ " / "+str(total)
 
	######################
	# CPU                # 
	######################	
	def SysCpuGetTimeList(self):
		statFile = file("/proc/stat", "r")
		timeList = statFile.readline().split(" ")[2:6]
		statFile.close()
		for i in range(len(timeList))  :
			timeList[i] = int(timeList[i])
		return timeList
	def SysCpu(self):
		try:
			x = self.SysCpuGetTimeList()
			sleep(2)
			y = self.SysCpuGetTimeList()
			for i in range(len(x)):
				y[i] -= x[i]
			cpuPct = 100 - (y[len(y) - 1] * 100.00 / sum(y))
		except:
			return "Error"
		return str('%.2f' %cpuPct)+"%"
 
	######################
	# Load Average       # 
	######################
	def SysLoadAvg(self):
		try:
		 f = open( "/proc/loadavg" )
		 contents = f.read().split()
		 f.close()
		except:
			return "Error"
		return contents[0]+" "+contents[1]+" "+contents[2];		
 
	######################
	# Systeme Uptime     # 
	######################
	def SysUptime(self):
		try:
			f = open( "/proc/uptime" )
			contents = f.read().split()
			f.close()
			total_seconds = float(contents[0])
			MINUTE  = 60
			HOUR    = MINUTE * 60
			DAY     = HOUR * 24
			days    = int( total_seconds / DAY )
			hours   = int( ( total_seconds % DAY ) / HOUR )
			minutes = int( ( total_seconds % HOUR ) / MINUTE )
			seconds = int( total_seconds % MINUTE )
			string = ""
			if days > 0:
				string += str(days) + "d "
			if len(string) > 0 or hours > 0:
				string += str(hours) + "h "
			if len(string) > 0 or minutes > 0:
				string += str(minutes) + "m "
			string += str(seconds) + "s "
		except:
			return "Error"
		return string;	
 
######################
# MAIN STARTER       # 
######################	
if __name__ == '__main__':
 
	si = SysInfo()
	si.start()
	q = str(raw_input('Press ENTER to quit program'))
	si.Stop()#!/usr/bin/python
