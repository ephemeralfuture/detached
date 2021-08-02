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

canvas.img = [PhotoImage(file="images/set0_0_0.png"), PhotoImage(file="images/set0_0_1.png"), PhotoImage(file="images/set0_0_2.png")]
canvas.moveit = [canvas.create_image(800,800,image=canvas.img[0], tags='background'), canvas.create_image(800,800,image=canvas.img[0], tags='background'), canvas.create_image(800,800,image=canvas.img[0], tags='background')]

#below is a 2D array of all the tags that will be used in this program. These will never update but need to be changed if the tags change.
the_tag_list = [["C3 45 33 0B", "96 5C 6D F0", "10 DD 44 36"],
                ["06 08 FE 3B", "B2 BB D9 3D", "76 D1 68 F0"],
                ["F0 C7 F6 35", "C2 53 A6 3D", "A6 65 9D F0"],
                ["46 9E 66 F0", "36 03 9D F0", "66 70 28 F0"],
                ["00 68 DD 36", "14 D0 6C 35", "04 09 94 35"],
                ["93 87 29 17", "73 87 58 15", "C4 52 84 30"]]
                 
display_part = [[0, 0, 0], [0, 0, 1], [0, 0, 2]]
'''
THAT'S THE VARIABLES ALL SET UP
'''
        
    

def update_image(this_set, this_image, this_reader):
    canvas.img[this_reader] = PhotoImage(file="images/set"+str(this_set)+"_"+str(this_image)+"_"+str(this_reader)+".png")
    canvas.moveit[this_reader] = canvas.create_image(700,600,image=canvas.img[this_reader], tags='background')
    #print("the current image for tag "+str(this_reader)+ " is " + str(this_set), str(this_image), str(this_reader))

for i in range(len(canvas.img)): #sets a base image when program starts
    update_image(0, i, 0)

def draw_canvas():
    #canvas.move(canvas.moveit[0], 3, 3)
    #canvas.move(canvas.moveit[1], -3, 3)
    #canvas.move(canvas.moveit[2], 1, -2)
    check_serial_inputs()
    canvas.after(20, draw_canvas)


def check_serial_inputs(): #check the input. The RFID cards are hard coded with a unique ID (UID) and this is what I am using here.
    
    global the_tag_list
    global display_part
    
    tag = ["not", "not", "not"] #set up an array with three strings, which will be changed in the for loop below
    
    tag0_read = ser0.readline()
    tag[0] = str(tag0_read)
    
    if "not" in str(tag0_read):
        display_part[0] = display_part[0]
    else:
        for i in the_tag_list:
            for j in i:
                if j in tag[0]:
                    display_part[0] = [the_tag_list.index(i), i.index(j), 0]
                    update_image(display_part[0][0], display_part[0][1], display_part[0][2])
                    
    #print("three readings are 1: " +tag[0] + ", 2: " + tag[1] + ", 3: " + tag[2])
    
    tag1_read = ser1.readline()
    tag[1] = str(tag1_read)

    if "not" in str(tag1_read):
        display_part[1] = display_part[1]
    else:
        for i in the_tag_list:
            for j in i:
                if j in tag[1]:
                    move_num = i.index(j)+1 # quite clunky function to change the reader but nowhere near as clunky as in tag 2!
                    if move_num > 2:
                        move_num = 0
                    display_part[1] = [the_tag_list.index(i), move_num, 1]
                    update_image(display_part[1][0], display_part[1][1], display_part[1][2])

    tag2_read = ser2.readline()
    tag[2] = str(tag2_read)

    if "not" in str(tag2_read):
        display_part[2] = display_part[2]
    else:
        for i in the_tag_list:
            for j in i:
                if j in tag[2]:
                    move_num = i.index(j) #a clunky function to change the iteration of the numbers - couldn't figure a better way!
                    if move_num == 0:
                        move_num = 2
                    elif move_num == 1:
                        move_num = 0
                    elif move_num == 2:
                        move_num = 1
                    display_part[2] = [the_tag_list.index(i), move_num, 2]
                    update_image(display_part[2][0], display_part[2][1], display_part[2][2])
    
    #print("tags read! 0: " + tag[0] + " 1: " + tag[1] + " 2: " + tag[2])
    
    ser0.flushInput()
    ser1.flushInput()
    ser2.flushInput()

draw_canvas()