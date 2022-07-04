

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import filedialog, ttk
import cv2

from picamera import PiCamera
from time import sleep


top=tk.Tk()
top.geometry('600x400')
top.title('Capturing Image')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)



camera = PiCamera()
camera.resolution = (600,600)


def one_image():
    camera.start_preview()
    for i in range(3):
        sleep(7)
        camera.capture('/home/pi/Downloads/upload files/chetan%s.png' % i)
        img = cv2.imread('/home/pi/Downloads/upload files/chetan%s.png' % i)
        #cropped_img = img[150:420,100:450]  #crops from (0,0) to (300,300)
        cv2.imwrite('/home/pi/test/chetan%s.png' % i,img)
    camera.stop_preview()

def twenty_image():
    camera.start_preview()
    for i in range(20):
        sleep(5)
        camera.capture('/home/pi/Downloads/upload files/chetan%s.png' % i)
        img = cv2.imread('/home/pi/Downloads/upload files/chetan%s.png' % i)
        #cropped_img = img[150:420,100:450]  #crops from (0,0) to (300,300)
        cv2.imwrite('/home/pi/train/chetan%s.png' % i,img)
    camera.stop_preview()




upload=Button(top,text="Train Image",command=twenty_image, padx=5,pady=5,width=30)
upload.configure(background='#364156', foreground='white', font=('arial',12,'bold'))
upload.pack(side=TOP, pady=15, ipady=15)

upload=Button(top,text="Test Image",command=one_image, padx=5,pady=5, width=30)
upload.configure(background='#364156', foreground='white', font=('arial',12,'bold'))
upload.pack(side=TOP, pady=15, ipady=15)

'''
upload=Button(top,text="Classify", padx=5,pady=5, width=30)
upload.configure(background='#364156', foreground='white', font=('arial',12,'bold'))
upload.pack(side=TOP, pady=15, ipady=15)

'''
upload=Button(top,text="Exit",command=quit, padx=5,pady=5, width=30)
upload.configure(background='#364156', foreground='white', font=('arial',12,'bold'))
upload.pack(side=TOP, pady=15, ipady=15)

top.mainloop()