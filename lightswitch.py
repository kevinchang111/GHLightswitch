from lightprofile import *
from threading import Thread,Lock
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import socket
import codecs
import signal
import sys

stop = False
#my enums
on = 0
off = 1
#set up google sheet
scope = ['https://spreadsheets.google.com/feeds/']
try:
	credentials = ServiceAccountCredentials.from_json_keyfile_name(credFileName,scope)
except:
	log("Bad credential file")
	exit(0)
	
on_signal = codecs.decode('0000002ad0f281f88bff9af7d5ef94b6c5a0d48bf99cf091e8b7c4b0d1a5c0e2d8a381f286e793f6d4eedfa2dfa2','hex') 
off_signal = codecs.decode('0000002ad0f281f88bff9af7d5ef94b6c5a0d48bf99cf091e8b7c4b0d1a5c0e2d8a381f286e793f6d4eedea3dea3','hex')
"""
prints argument and concat time behind it
args:
	s: the string to print
Return value: None
"""
def log(s):
	try:
		f=open('log.log','a')
		f.write(s+"   "+currTime()+"\n")
		print(s+"   "+currTime())
		f.close()
		del f
	except:
		print("Bad log file")
		
"""
Returns current time in form of DATE MONTH YEAR TIME
"""
def currTime():
	return time.strftime("%d %b %y %H:%M:%S",time.localtime())
"""
Attempts to authorize access to spreadsheet. If fail, sleeps and retries in 60secs
Return value:
	worksheet
"""
def auth():
	try:
		log("Auth-ing")
		gc = gspread.authorize(credentials)
		wks = gc.open(lightsSheet).sheet1
	except Exception as e:
		log("Auth fail...retrying in 60secs"+str(e.args))
		time.sleep(60)
		if stop:
			exit(0)
		auth()
	return wks
"""
Sends a signal to plugIP:plugPort of either on or off 
and updates the row in google sheet to be "DONE" on 2nd column 
args:
	worksheet: worksheet object being worked on
	index: row of "ON" signal (latest row) to update with "DONE"
	status: on(0) or off(1)
"""
def sendSignal(worksheet ,index, status):
	wks = worksheet
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((plugIP,plugPort))
	except socket.error as e:
		if stop:
			return
		log("CONNECTION ERROR...retrying in 60secs"+string(status))
		time.sleep(60)
		sendSignal(string(index)+string(status))
	if status == on:
		log("ON")
		s.send(on_signal)
	else:
		log("OFF")
		s.send(off_signal)
	wks.update_acell("B"+str(index),"DONE")
	s.close()

"""
Traverses down rows to find the first row that is not "DONE" on 2nd column
Infinite loop and when 1st column of that row is "ON"/"OFF" it calls sendSignal with corresponding params (which turns on the light and updates DONE)
"""
def worker():
	wks = auth()
	curr = 1
	log("Start")
	while True:
		if(stop):
			 return
		try:	
			while(wks.acell("B"+str(curr)).value=="DONE"): 
				curr+=1
			
			curr_value = wks.acell("A"+str(curr)).value 
			if(curr_value!= ""):
				if(curr_value == "ON"):
					sendSignal(wks, curr, on)
				if(curr_value == "OFF"):
					sendSignal(wks, curr,off)
				
			time.sleep(1)
		except Exception as e:
			log("Worker exception"+str(e.args))
			wks = auth()
			time.sleep(10)			
"""
SIGINT handler - sets global "stop" to value True
"""
def sigint_handler(signal,frame):
	log("Stop (SIGINT)")
	global stop
	stop = True
	log("PROGRAM STOPPED")

if __name__=="__main__":
	log("\nPROGRAM START")
	signal.signal(signal.SIGINT,sigint_handler)
	worker()
#	while True:
#		signal.pause()
