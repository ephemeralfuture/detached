#!/usr/bin/python

'''
This is the code for an artwork about detatchment in a technological world.
It takes input from three serial ports and outputs images on a monitor.
It was built in 2021 as part of a residency with Leitrim Sculpture Centre, Manorhamilton,
by Irish visual artist Shane Finan.

'''

from tkinter import * #tkinter is the GUI control
from PIL import Image #Pillow is a library for image manipulation
import os #to run commands on the operating system
import time #to get and use current time
import serial #serial input - taking reading from arduino
#import threading #for intermittently checking Arduino

root= Tk()
canvas = Canvas(root) #set up the canvas (the frame inside the window)
ser0 = serial.Serial('/dev/ttyACM0', 9600) #declaring the Arduinos
ser1 = serial.Serial('/dev/ttyACM1', 9600)
ser2 = serial.Serial('/dev/ttyACM2', 9600)

scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()

frame = Frame(root)
frame.pack()
    
canvas = Canvas(root, width=scrwidth, height=scrheight, borderwidth=0, bg="black")
canvas.pack()


root.geometry("%dx%d"%(scrwidth, scrheight))
root.configure(bg='black')
root.attributes('-fullscreen', True)

curr_tag = ["C3", "C3", "C3"] #an array for the RFID tags
canvas.img = [PhotoImage(file="images/set0_0_0.png"), PhotoImage(file="images/set0_0_1.png"), PhotoImage(file="images/set0_0_2.png")]
canvas.moveit = [canvas.create_image(800,800,image=canvas.img[0], tags='background'), canvas.create_image(800,800,image=canvas.img[0], tags='background'), canvas.create_image(800,800,image=canvas.img[0], tags='background')]

uptimer = 0

'''
THAT'S THE VARIABLES ALL SET UP
'''
        
    

def update_image(this_reader, this_image):
    canvas.img[this_reader] = PhotoImage(file="images/"+str(this_image)+str(this_reader)+".png")
    canvas.moveit[this_reader] = canvas.create_image(700,600,image=canvas.img[this_reader], tags='background')

for i in range(len(curr_tag)):
    update_image(i, "set0_0_")

def draw_canvas():
    #canvas.move(canvas.moveit[0], 3, 3)
    #canvas.move(canvas.moveit[1], -3, 3)
    #canvas.move(canvas.moveit[2], 1, -2)
    check_serial_inputs()
    canvas.after(20, draw_canvas)
 

'''def update_image():
   for i in range(len(curr_tag)):
       canvas.img[i] = PhotoImage(file="images/jelly"+str(i)+".png")
       canvas.moveit[i] = canvas.create_image(800,800,image=canvas.img[i], tags='background') 
'''

def check_current_set(tag): #checks the set of images currently in use by a tag
    if "C3" in tag or "10" in tag or "96" in tag:
        return 0
    elif "06" in tag or "B2" in tag or "76" in tag:
        return 1
    elif "F0" in tag or "C2" in tag or "A6" in tag:
        return 2
    elif "46" in tag or "36" in tag or "66" in tag:
        return 3
    elif "00" in tag or "14" in tag or "04" in tag:
        return 4
    elif "93" in tag or "73" in tag or "C4" in tag:
        return 5

def check_serial_inputs(): #check the input. The RFID cards are hard coded with a unique ID (UID) and this is what I am using here.

    global curr_tag
    past_tag = [curr_tag[0], curr_tag[1], curr_tag[2]] #check if tag has changed
    
    ''' TAG 0
        FOLLOWS
        '''
    tag0 = ser0.readline()
    try:
        tag0 = tag0[11:12]
    except:
        "not" in str(tag0)
        
    if "not" not in str(tag0) and past_tag[0] not in str(tag0):
        tag_read = str(tag0)
        print("this is tag 0: " + tag_read)
        try:
            print("the UID I'm using is " + tag_read[11])
        except:
           return

        this_set = check_current_set(tag_read)
        print("the set reading is " +str(this_set))
        
        #set0
        if "C3" in tag_read:
            curr_tag[0] = "C3"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "10" in tag_read:
            curr_tag[0] = "10"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "96" in tag_read:
            curr_tag[0] = "96"
            update_image(0, "set"+str(this_set)+"_2_")
            
        #set 1
        if "06" in tag_read:
            curr_tag[0] = "06"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "B2" in tag_read:
            curr_tag[0] = "B2"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "76" in tag_read:
            curr_tag[0] = "76"
            update_image(0, "set"+str(this_set)+"_2_")
        
        #set 2
        if "F0" in tag_read:
            curr_tag[0] = "F0"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "C2" in tag_read:
            curr_tag[0] = "C2"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "A6" in tag_read:
            curr_tag[0] = "A6"
            update_image(0, "set"+str(this_set)+"_2_")
        
        #set 3
        if "46" in tag_read:
            curr_tag[0] = "46"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "36" in tag_read:
            curr_tag[0] = "36"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "66" in tag_read:
            curr_tag[0] = "66"
            update_image(0, "set"+str(this_set)+"_2_")
        
        #set 4
        if "00" in tag_read:
            curr_tag[0] = "00"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "14" in tag_read:
            curr_tag[0] = "14"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "04" in tag_read:
            curr_tag[0] = "04"
            update_image(0, "set"+str(this_set)+"_2_")
        
        #set 5
        if "93" in tag_read:
            curr_tag[0] = "93"
            update_image(0, "set"+str(this_set)+"_0_")
        elif "73" in tag_read:
            curr_tag[0] = "73"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "C4" in tag_read:
            curr_tag[0] = "C4"
            update_image(0, "set"+str(this_set)+"_2_")
    
    ''' TAG 1
        FOLLOWS
        '''
    tag1 = ser1.readline()
    try:
        tag1 = tag1[11:12]
    except:
        "not" in str(tag1)
    
    if "not" not in str(tag1) and past_tag[1] not in str(tag1):
        tag_read = str(tag1)
        print("this is tag 1: " + tag_read)
        
        this_set = check_current_set(tag_read)
        
        #set0
        if "96" in tag_read:
            curr_tag[1] = "96"
            update_image(1, "set"+str(this_set)+"_0_")
        elif "C3" in tag_read:
            curr_tag[1] = "C3"
            update_image(1, "set"+str(this_set)+"_1_")
        elif "10" in tag_read:
            curr_tag[1] = "10"
            update_image(1, "set"+str(this_set)+"_2_")
        
        #set 1
        if "06" in tag_read:
            curr_tag[0] = "06"
            update_image(0, "set"+str(this_set)+"_1_")
        elif "B2" in tag_read:
            curr_tag[0] = "B2"
            update_image(0, "set"+str(this_set)+"_2_")
        elif "76" in tag_read:
            curr_tag[0] = "76"
            update_image(0, "set"+str(this_set)+"_0_")
        
        #set 2
        if "F0" in tag_read:
            curr_tag[1] = "F0"
            update_image(1, "set"+str(this_set)+"_1_")
        elif "C2" in tag_read:
            curr_tag[1] = "C2"
            update_image(1, "set"+str(this_set)+"_2_")
        elif "A6" in tag_read:
            curr_tag[1] = "A6"
            update_image(1, "set"+str(this_set)+"_0_")
        
        #set 3
        if "46" in tag_read:
            curr_tag[1] = "46"
            update_image(1, "set"+str(this_set)+"_1_")
        elif "36" in tag_read:
            curr_tag[1] = "36"
            update_image(1, "set"+str(this_set)+"_2_")
        elif "66" in tag_read:
            curr_tag[1] = "66"
            update_image(1, "set"+str(this_set)+"_0_")
        
        #set 4
        if "00" in tag_read:
            curr_tag[1] = "00"
            update_image(1, "set"+str(this_set)+"_1_")
        elif "14" in tag_read:
            curr_tag[1] = "14"
            update_image(1, "set"+str(this_set)+"_2_")
        elif "04" in tag_read:
            curr_tag[1] = "04"
            update_image(1, "set"+str(this_set)+"_0_")
        
        #set 5
        if "93" in tag_read:
            curr_tag[1] = "93"
            update_image(1, "set"+str(this_set)+"_1_")
        elif "73" in tag_read:
            curr_tag[1] = "73"
            update_image(1, "set"+str(this_set)+"_2_")
        elif "C4" in tag_read:
            curr_tag[1] = "C4"
            update_image(1, "set"+str(this_set)+"_0_")
        else:
            curr_tag[0] = curr_tag[0]
  
  
  
    ''' TAG 2
        FOLLOWS
        '''
    tag2 = ser2.readline()
    try:
        tag2 = tag2[11:12]
    except:
        "not" in str(tag2)
    
    if "not" not in str(tag2)  and past_tag[2] not in str(tag2):
        tag_read = str(tag2)
        print("this is tag 2: " + tag_read)
        
        this_set = check_current_set(tag_read)
        
        #set0
        if "10" in tag_read:
            curr_tag[2] = "10"
            update_image(2, "set"+str(this_set)+"_0_")
        elif "96" in tag_read:
            curr_tag[2] = "96"
            update_image(2, "set"+str(this_set)+"_1_")
        elif "C3" in tag_read:
            curr_tag[2] = "C3"
            update_image(2, "set"+str(this_set)+"_2_")
        else:
            curr_tag[1] = curr_tag[1]
        
        #set 2
        if "F0" in tag_read:
            curr_tag[2] = "F0"
            update_image(2, "set"+str(this_set)+"_2_")
        elif "C2" in tag_read:
            curr_tag[2] = "C2"
            update_image(2, "set"+str(this_set)+"_0_")
        elif "A6" in tag_read:
            curr_tag[2] = "A6"
            update_image(2, "set"+str(this_set)+"_1_")
        
        #set 3
        if "46" in tag_read:
            curr_tag[2] = "46"
            update_image(2, "set"+str(this_set)+"_2_")
        elif "36" in tag_read:
            curr_tag[2] = "36"
            update_image(2, "set"+str(this_set)+"_0_")
        elif "66" in tag_read:
            curr_tag[2] = "66"
            update_image(2, "set"+str(this_set)+"_1_")
        
        #set 4
        if "00" in tag_read:
            curr_tag[2] = "00"
            update_image(2, "set"+str(this_set)+"_2_")
        elif "14" in tag_read:
            curr_tag[2] = "14"
            update_image(2, "set"+str(this_set)+"_0_")
        elif "04" in tag_read:
            curr_tag[2] = "04"
            update_image(2, "set"+str(this_set)+"_1_")
        
        #set 5
        if "93" in tag_read:
            curr_tag[2] = "93"
            update_image(2, "set"+str(this_set)+"_2_")
        elif "73" in tag_read:
            curr_tag[2] = "73"
            update_image(2, "set"+str(this_set)+"_0_")
        elif "C4" in tag_read:
            curr_tag[2] = "C4"
            update_image(2, "set"+str(this_set)+"_1_")
    
    ser0.flush()
    ser1.flush()
    ser2.flush()

draw_canvas()