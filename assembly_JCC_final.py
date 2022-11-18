#!/usr/bin/python

'''
Adapted from two past interactive artworks, this is the code for the 
interactive work 'Assembly' by Shane Finan.

The past works were 'it seemed like we were moving closer together'
and 'faigh ar ais as an fharraige'. Both are available publicly on Github.

This work was created for the Jackie Clarke Collection in response 
to the idea of story, memory, printed matter, and museum collections.

It was launched in November 2022.

Funded by Mayo Arts Office and Decade of Centenaries funding.
'''

import os #to run commands on the operating system
import time #to get and use current time
import serial #serial input - taking reading from arduino

from math import sqrt, floor, ceil #a bit of maths
import random

import paramiko #used for SSH management

ser0 = serial.Serial('/dev/ttyACM0', 9600) #declaring the Arduino

#below is a 2D array of all the tags that will be used in this program. These will never update but need to be changed if the tags change.
the_tag_list = ["B2 F6 BD 3D", "10 91 E0 36", "36 DD 85 F0", "03 D8 65 15", "00 32 A7 36"]
kill_tag = "D9 69 DB C2" #the tag for killing the program outright

#Next two blocks are the variables to set up SSH into the two linked Raspberry Pis
ssh0 = paramiko.SSHClient()
ssh0.load_system_host_keys()
ssh0.connect(hostname="192.168.0.71", username="pi", password="assembly")

ssh1 = paramiko.SSHClient()
ssh1.load_system_host_keys()
ssh1.connect(hostname="192.168.0.72", username="pi", password="assembly")

ssh_proj = paramiko.SSHClient()
ssh_proj.load_system_host_keys()
ssh_proj.connect(hostname="192.168.0.75", username="pi", password="assembly")

timer = 995

selected_film = "none"

started = False
                 
'''
THAT'S THE VARIABLES ALL SET UP
'''


def check_serial_inputs(): #check the input. The RFID cards are hard coded with a unique ID (UID) and this is what I am using here.
	
	global the_tag_list
	global timer
	global selected_film
	curr_film = "none"
	
	tag0 = "not" #set up an array with a string, which will be changed in the for loop below
	tag0_read = ser0.readline()
	tag0 = str(tag0_read);
	
	if "not" in tag0:
		curr_film = "none"
	if selected_film in tag0:
		return
	else:
		if curr_film not in tag0:
			curr_film = tag0
			play_films(curr_film)
			selected_film = curr_film
		if kill_tag in tag0:
			shutdown_all()
	print("tag read is " + tag0)
	
	ser0.flushInput()


def play_films(curr_film):
	omx_arguments = "omxplayer --loop -o local --no-osd "
	(stdin, stdout, stderr) = ssh0.exec_command("killall omxplayer.bin")    
	(stdin, stdout, stderr) = ssh1.exec_command("killall omxplayer.bin")
	(stdin, stdout, stderr) = ssh_proj.exec_command("killall omxplayer.bin")
	for x in range(5):
		if the_tag_list[x] in curr_film:
			curr_film = "card"+str(x)+"_"
	jcc_film_path_set = "Desktop/jcc/" + "" + curr_film + ".mp4"
	jcc_film_path_random = "Desktop/jcc/procedural" + str(random.randint(0, 50)) + ".mp4"
	(stdin, stdout, stderr) = ssh0.exec_command(omx_arguments+jcc_film_path_set)
	(stdin, stdout, stderr) = ssh1.exec_command(omx_arguments+jcc_film_path_random)
	(stdin, stdout, stderr) = ssh_proj.exec_command(omx_arguments+jcc_film_path_set)

def reset_films():
	omx_arguments = "omxplayer --loop -o local --no-osd "
	(stdin, stdout, stderr) = ssh0.exec_command("killall omxplayer.bin")    
	(stdin, stdout, stderr) = ssh1.exec_command("killall omxplayer.bin")
	(stdin, stdout, stderr) = ssh_proj.exec_command("killall omxplayer.bin")
	(stdin, stdout, stderr) = ssh0.exec_command(omx_arguments+"Desktop/jcc/reset.mp4")
	(stdin, stdout, stderr) = ssh1.exec_command(omx_arguments+"Desktop/jcc/reset.mp4")
	(stdin, stdout, stderr) = ssh_proj.exec_command(omx_arguments+"Desktop/jcc/reset.mp4")
	
def shutdown_all():
	(stdin, stdout, stderr) = ssh0.exec_command("sudo shutdown -h -P now")
	(stdin, stdout, stderr) = ssh1.exec_command("sudo shutdown -h -P now")
	#the projector pi stays on!!!
	#os.system("shutdown -h -P now") this pi also stays on, for now!

def main():
	global started
	if started is False:
		(stdin, stdout, stderr) = ssh0.exec_command("xpdf -fullscreen Desktop/jcc/newspaper.pdf")
		(stdin, stdout, stderr) = ssh1.exec_command("xpdf -fullscreen Desktop/jcc/newspaper2.pdf")
		(stdin, stdout, stderr) = ssh_proj.exec_command("xpdf -fullscreen Desktop/jcc/newspaper_proj.pdf")
		started = True
	check_serial_inputs()
	global timer
	timer = timer+1
	time.sleep(0.5)
	if timer > 1000:
		reset_films()
		timer = 0

while __name__ == '__main__':
	main()
