import ctypes
import os
from tkinter import *
from tkinter import filedialog, ttk
import cv2
import numpy as np
import scipy.signal
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

root = Tk()
ttk.Style().configure("TButton", justify=CENTER)

# Global variables
gui_width = 1300
gui_height = 500
ip_file = ""
op_file = ""
original_img = None
modified_img = None
user_arg = None
popup = None
popup_input = None


root.title("Image Processing")
# root.geometry(f"{gui_width}x{gui_height}")
# root.resizable(False, False)
root.minsize(gui_width, gui_height)


def set_user_arg():
    global user_arg
    user_arg = popup_input.get()
    popup.destroy()
    popup.quit()


def open_popup_input(text):
    global popup, popup_input
    popup = Toplevel(root)
    popup.resizable(False, False)
    popup.title("User Input")
    text_label = ttk.Label(popup, text=text, justify=LEFT)
    text_label.pack(side=TOP, anchor=W, padx=15, pady=10)
    popup_input = ttk.Entry(popup)
    popup_input.pack(side=TOP, anchor=NW, fill=X, padx=15)
    popup_btn = ttk.Button(popup, text="OK", command=set_user_arg).pack(pady=10)
    popup.geometry(f"400x{104+text_label.winfo_reqheight()}")
    popup_input.focus()
    popup.mainloop()


def draw_before_canvas():
    global original_img, ip_file
    original_img = Image.open(ip_file)
    original_img = original_img.convert("RGB")
    img = ImageTk.PhotoImage(original_img)
    before_canvas.create_image(
        256,
        256,
        image=img,
        anchor="center",
    )
    before_canvas.img = img


def draw_after_canvas(mimg):
    global modified_img

    modified_img = Image.fromarray(mimg)
    img = ImageTk.PhotoImage(modified_img)
    after_canvas.create_image(
        256,
        256,
        image=img,
        anchor="center",
    )
    after_canvas.img = img


def load_file():
    global ip_file
    ip_file = filedialog.askopenfilename(
        title="Open an image file",
        initialdir=".",
        filetypes=[("All Image Files", "*.*")],
    )
    draw_before_canvas()
    # print(f"Image loaded from: {ip_file}")


def save_file():
    global ip_file, original_img, modified_img
    file_ext = os.path.splitext(ip_file)[1][1:]
    op_file = filedialog.asksaveasfilename(
        filetypes=[
            (
                f"{file_ext.upper()}",
                f"*.{file_ext}",
            )
        ],
        defaultextension=[
            (
                f"{file_ext.upper()}",
                f"*.{file_ext}",
            )
        ],
    )
    modified_img = modified_img.convert("RGB")
    modified_img.save(op_file)
    # print(f"Image saved at: {op_file}")


# frames
left_frame = ttk.LabelFrame(root, text="Original Image", labelanchor=N)
left_frame.pack(fill=BOTH, side=LEFT, padx=10, pady=10, expand=1)

middle_frame = ttk.LabelFrame(root, text="Image Processing", labelanchor=N)
middle_frame.pack(fill=BOTH, side=LEFT, padx=5, pady=10)

right_frame = ttk.LabelFrame(root, text="Modified Image", labelanchor=N)
right_frame.pack(fill=BOTH, side=LEFT, padx=10, pady=10, expand=1)

# left frame contents
before_canvas = Canvas(left_frame, bg="#CDCDCD", width=535, height=535)
before_canvas.pack(expand=1)


browse_btn = ttk.Button(left_frame, text="Browse", command=load_file)
browse_btn.pack(expand=1, anchor=SW, pady=(5, 0))
#browse_btn.pack(expand=1, anchor=SW, ipady=50,ipadx=50)

# middle frame contents
algo_canvas = Canvas(middle_frame, width=260, highlightthickness=0)
scrollable_algo_frame = Frame(algo_canvas)
scrollbar = Scrollbar(
    middle_frame, orient="vertical", command=algo_canvas.yview, width=15
)
scrollbar.pack(side="right", fill="y")
algo_canvas.pack(fill=BOTH, expand=1)
algo_canvas.configure(yscrollcommand=scrollbar.set)
algo_canvas.create_window((0, 0), window=scrollable_algo_frame, anchor="nw")
scrollable_algo_frame.bind(
    "<Configure>", lambda _: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
)


# right frame contents
after_canvas = Canvas(right_frame, bg="#CDCDCD", width=535, height=535)
after_canvas.pack(expand=1)

#import tkinter as tk 
#from tkinter import ttk
style = ttk.Style()
#root = tk.Tk()
style.theme_use('alt')
style.configure("TButton",background = "cyan",foreground = "black")
save_btn = ttk.Button(right_frame, text="Save", command=save_file)
save_btn.pack(expand=1, anchor=SE, pady=(5, 0))
#save_btn.pack(expand=1, anchor=SE, ipady=50,ipadx=50)


# gray

def gray_scale(img):
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def callRGB2Gray():
    img = cv2.imread(ip_file)
    grayscale = gray_scale(img)
    draw_after_canvas(grayscale)

# reduce noise in the image
def reduce_noise(img):
    gray = gray_scale(img)
    noise = cv2.fastNlMeansDenoising(gray)
    return noise

def callDenoise():
    img = cv2.imread(ip_file)
    noise = reduce_noise(img)
    noise=cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)
    draw_after_canvas(noise)

# histogram equalization
def equalize_hist(img, kernel):
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

def callEquiHist():
    img = cv2.imread(ip_file)
    noise = reduce_noise(img)
    noise = cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)
    kernel = np.ones((7,7),np.uint8)
    hist = equalize_hist(noise,kernel)
    draw_after_canvas(hist)

# invert a binary image
def invert(img):
    return cv2.bitwise_not(img)

def callInvert():
    img = cv2.imread(ip_file)
    noise = reduce_noise(img)
    cl2=CLAHE(noise)
    inv=invert(cl2)
    draw_after_canvas(inv)





# skeletonize the image
def skel():
    img = cv2.imread(ip_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noise = cv2.fastNlMeansDenoising(gray)
    noise = cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)
    '''
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8,8))  #Define tile size and clip limit. 
    cl1 = clahe.apply(noise)
    inv = cv2.bitwise_not(cl1)
    '''
    kernel = np.ones((3,3),np.uint8)
    img = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    inv = cv2.bitwise_not(img_output)
    
    gray_scale = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
    img = gray_scale.copy()
    skel = img.copy()
    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
    iterations = 0

    while True:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        if cv2.countNonZero(img) == 0:
            break
    draw_after_canvas(skel)

def callThresh():
    img = cv2.imread(ip_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noise = cv2.fastNlMeansDenoising(gray)
    noise = cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)
    '''
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8,8))  #Define tile size and clip limit. 
    cl1 = clahe.apply(noise)
    inv = cv2.bitwise_not(cl1)
    '''
    kernel = np.ones((3,3),np.uint8)
    img = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    inv = cv2.bitwise_not(img_output)
    
    gray_scale = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
    img = gray_scale.copy()
    skel = img.copy()
    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
    iterations = 0

    while True:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        if cv2.countNonZero(img) == 0:
            break
    thr=thresh(skel)
    draw_after_canvas(thr)



# threshold to make the veins more visible
def thresh(img):
    _, thr = cv2.threshold(img, 5,255, cv2.THRESH_BINARY)
    return thr
#CLAHE
def CLAHE(noise):
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8,8))  #Define tile size and clip limit. 
    cl1 = clahe.apply(noise)
    return cl1

def callCLAHE():
    img = cv2.imread(ip_file)
    noise = reduce_noise(img)
    cl2=CLAHE(noise)
    draw_after_canvas(cl2)


def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished

        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            #cv2.imshow("Cropped", roi)
            draw_after_canvas(roi)

def callCrop():
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    img = cv2.imread(ip_file)
    oriImage = img.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0

    cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)


ttk.Button(
    scrollable_algo_frame, text="Grayscale", width=40, command=callRGB2Gray
).pack(expand=1, padx=10, pady=10, ipady=4)

ttk.Button(
    scrollable_algo_frame,
    text="Denoise",
    width=40,
    command=callDenoise,
).pack(pady=10, ipady=10)

ttk.Button(
    scrollable_algo_frame,
    text="Equalize histogram",
    width=40,
    command=callEquiHist,
).pack(pady=10, ipady=10)

ttk.Button(
    scrollable_algo_frame,
    text="CLAHE",
    width=40,
    command=callCLAHE,
).pack(pady=10, ipady=10)

ttk.Button(
    scrollable_algo_frame,
    text="Invert",
    width=40,
    command=callInvert,
).pack(pady=10, ipady=10)

ttk.Button(
    scrollable_algo_frame,
    text="Skeleton",
    width=40,
    command=skel,
).pack(pady=10, ipady=10)

ttk.Button(
    scrollable_algo_frame,
    text="Threshold",
    width=40,
    command=callThresh,
).pack(pady=10, ipady=10)


root.mainloop()