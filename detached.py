'''
This is the code for an artwork about detatchment in a technological world.
It takes input from three serial ports and outputs images on a monitor.
It was built in 2021 as part of a residency with Leitrim Sculpture Centre, Manorhamilton,
by Irish visual artist Shane Finan. The code borrows heavily from an image selector in
tkinter (Python) by Giovanni Python at the following link:
https://pythonprogramming.altervista.org/imageslider-3-0-tkinter-app-to-show-images-like-in-a-presentation/?doing_wp_cron=1627635490.8990950584411621093750



Because of the link to key bindings, to make things simple I have used a key controller library to bind key events to srial read.
'''

import tkinter as tk #tkinter for interface/GUI
#import glob
from PIL import Image, ImageTk #PIL is pillow, an image displaying and manipulating library
import os #to run commands on the operating system
import time #to get and use current time
import serial #serial input - taking reading from arduino
#from pynput.keyboard import Key, Controller #to simulate keys being pressed

root = tk.Tk() #set up tk
canvas = tk.Canvas(root) #set up the canvas (the frame)
ser0 = serial.Serial('/dev/ttyACM0', 9600)
ser1 = serial.Serial('/dev/ttyACM1', 9600)
this_image = 0
#keyboard = Controller()

curr_tag = [0, 0, 0] #an array for the RFID tags

def get_window_size():
    if root.winfo_width() > 200 and root.winfo_height() >30:
        w = root.winfo_width() - 200
        h = root.winfo_height() - 30
    else:
        w = 200
        h = 30
    return w, h


def showimg():
    global curr_tag
    for i in curr_tag: #for loop for scalability in future
        this_image = select_images(curr_tag[i])
        img_location = "images/" + this_image
        img = ImageTk.PhotoImage(Image.open(img_location))
        canvas.image = img
        canvas.config(width=1200, height=800)
        canvas.create_image(0, 0, image=img, anchor=tk.NW)
        canvas.configure(bg='black')
        
    canvas.pack()
    
    
def check_serial_inputs(): #check the input. The RFID cards are hard coded with a unique ID (UID) and this is what I am using here.
    global curr_tag
    
    tag0_read = str(ser0.readline())
    print("this is tag 0: " + tag0_read)
    
    if "jelly" in tag0_read:
        curr_tag[0] = 0
    elif "93" in tag0_read:
        curr_tag[0] = 1
    else:
        curr_tag[0] = curr_tag[0]
    
    tag1_read = str(ser1.readline())
    print("this is tag 1: " + tag1_read)
    
    if "C3" in tag1_read:
        curr_tag[1] = 1
    elif "93" in tag1_read:
        curr_tag[1] = 0
    else:
        curr_tag[1] = curr_tag[1]

def select_images(tags): #a function to manually choose what images appear with what cards. This can't really be automated because it is chosen for aesthetic/variable mixes
    if tags == 0 or tags == None:
        return "jelly" + str(tags) + ".png"
    elif tags == 1:
        return "food.jpg"
    elif tags == 2:
        return "mountain.jpg"
    else:
        return "beach.jpg"

def main():
    while True:
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry("%dx%d"%(width, height))
        root.configure(bg='black')
        root.attributes('-fullscreen', True)
        
        global curr_tag
        check_serial_inputs()
        showimg()
        
        canvas.pack()
        
        root.update()

def close(event):
    root.withdraw()
    
root.bind("<Escape>", close)

main()
