from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import filedialog
import os




main = tkinter.Tk()
main.title("vehicle Speed, count & plate Detection")
main.geometry("1300x1200")

def numPlate():
    os.system("python numplate.py")

def speedCheck():
    os.system("python speed_check.py")

def countveh():
    os.system("python count_speed.py")
def Helmet_detection():
    os.system("python Helmet_detection.py")
    
def close():
    main.destroy()

font = ('times', 16, 'bold')
title = Label(main, text='VEHICLE SPEED, COUNT & NUMBER PLATE DETECTION')
title.config(bg='#8E44AD', fg='#F4D03F')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
Speed = Button(main, text="vehicle Speed", command=speedCheck)
Speed.place(x=100,y=200)
Speed.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='DarkOrange1', fg='white')  
pathlabel.config(font=font1)           

processButton = Button(main, text="vehicle Number Plate", command=numPlate)
processButton.place(x=300,y=200)
processButton.config(font=font1) 


predictButton = Button(main, text="Vehicle Count", command=countveh)
predictButton.place(x=600,y=200)
predictButton.config(font=font1)

HelmetButton = Button(main, text="Helmet Predict", command=Helmet_detection)
HelmetButton.place(x=800,y=200)
HelmetButton.config(font=font1)

closeButton = Button(main, text="Close", command=close)
closeButton.place(x=1000,y=200 )
closeButton.config(font=font1)


main.config(bg='skyblue')
main.mainloop()
