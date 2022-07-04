import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy
#from keras.datasets import cifar10
import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
model = load_model("model.h5")

class_names={
0 : 'abhijeet',
1 : 'adi',
2 : 'akash',
3 : 'ashutosh',
4 :'chetan',
5 : 'deepak',
6 : 'dilip'
}

top=tk.Tk()
top.geometry('800x600')
top.title('Palm Vein Recognition System')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD',foreground='cyan', font=('arial',15,'bold'))
sign_image = Label(top)



#pic = np.array(Image.open("/content/drive/MyDrive/test/dilip8.png"))
#img = cv2.imread("chetan4.png",0)


def classify(file_path):
    global label_packed
    classes=[]
    img = cv2.imread(file_path,0)
    pic = cv2.resize(img,(224,224))
    pic=np.float32(pic)
    test_images = np.array([pic])
    test_images = test_images.reshape(-1, 224,224, 1)
    #print ("predicting result")
    test_images = test_images / np.max(test_images)
    predictions = model.predict(test_images)
    classes.append(np.argmax(predictions))
    name=classes[0]
    sign = class_names[name]
    print(sign)
    label.configure(foreground='cyan', text=sign)

def show_classify_button(file_path):
    classify_b=Button(top,text="Classify Image", command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='cyan', foreground='black', font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)

def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass

upload=Button(top,text="Upload an image",command=upload_image, padx=10,pady=5)
upload.configure(background='cyan', foreground='black', font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Palm Vein Recognition System",pady=20, font=('arial',20,'bold'))

heading.configure(background='#CDCDCD',foreground='cyan')
heading.pack()
top.mainloop()