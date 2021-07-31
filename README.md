# detatched

RFID Pi setup guide
This is the guide for setting up Raspberry Pis for the project "Detached Touch". It is run from three Arduinos all running the same code with RFID tag readers attached, one Raspberry Pi, a Python script and a monitor.

The following is a step-by-step for setting up the Raspberry Pi.

This repository also contains the latest Arduino code for reading the RFID readers, and the Python script for displaying output on a monitor

1) Install RFID and get this running - I borrowed from Rui Santos' code here: https://randomnerdtutorials.com/security-access-using-mfrc522-rfid-reader-with-arduino/

The code should print a line with the UID of the RFID tag. This is later read as a string by Python, so any printout of the UID will work. However, the UIDs will need to be updated for each individual piece as these are manually made outside the installation (three cards all correspond to one another but it is not immediately obvious how)

------------------------------------
Using Python3 with TKinter

No more Python2 so forget about it!

tkinter is already on the Raspberry Pi, but at some later time might need to be manually installed.

A third shot - Pillow (for manipulating images)
	pip3 install pillow (turns out this is already on Pi)

ImageTk in Pillow is Not working on latest Raspi image so you need to install the new libraries:
	sudo apt-get install python-imaging python-imaging-tk ***NB very important***
	

So far so good. I have this working, and with Serial.

The modules needed are all documented in the Python script. Some documentation of the finished piece will be put up at some later time.
