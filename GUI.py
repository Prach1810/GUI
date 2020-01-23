from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
from tkinter.ttk import Combobox
import threading
import time
import imutils
import socket
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #NavigationToolbar2TkAgg
from matplotlib.figure import Figure


host = socket.gethostname()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("10.4.58.52",12346))
s.listen(5)
c,addr=s.accept()


global cb
global w

# initialize the root window and image panel
root = tki.Tk()
panel = None

#different windows

def create_window1(event):
    window1 = tki.Toplevel(root)
    window1.title('Laser')
    window1.geometry('650x500')
    c.sendall("l".encode())
    v= c.recv(1024).decode()
    print(v)
    l=tki.Label(window1, text=v)
    l.pack()
    
    """
    # if you want to add a graph
    figure = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, window1)
    chart_type.get_tk_widget().pack()
    ax.set_title('The Title of your chart')
    #df.plot(kind='line', legend=True, ax=ax)
    """

def create_window2(event):
    window2 = tki.Toplevel(root)
    window2.title('Gas Analyzer')
    window2.geometry('650x500')
    c.sendall("g".encode())
    v= c.recv(1024).decode()
    print(v)
    l=tki.Label(window2, text=v)
    l.pack()
    

def create_window3(event):
    window3 = tki.Toplevel(root)
    window3.title('Controler')
    window3.geometry('650x500')
    #window3.configure(bg="LightCyan2")
    #rightFrame = tki.Frame(window3,width=600, height = 370)
    
    # create buttons, that when pressed, will control movement
    
    up = tki.Button(window3, text=" ^ ",command=moveup)
    up.place(x = 300, y = 50)
    #up.bind("u",move(0))
    up.config(height = 2, width = 2,bg = "powder blue", fg = "steel blue")
    
    down = tki.Button(window3, text=" v",command=movedown)
    down.place(x = 300, y = 350)
    down.config(height = 2, width = 2,bg = "powder blue", fg = "steel blue")

    left = tki.Button(window3, text=" < ", command=moveleft)
    left.place(x = 100, y = 200)
    left.config(height = 2, width = 2,bg = "powder blue", fg = "steel blue")

    right= tki.Button(window3, text=" > ", command=moveright)
    right.place(x = 500, y = 200)
    right.config(height = 2, width = 2,bg = "powder blue", fg = "steel blue")

    stop= tki.Button(window3, text=" Stop ", command=movestop)
    stop.place(x = 300, y = 200)
    stop.config(height = 2, width = 2,bg = "powder blue", fg = "steel blue")


def print_value(val): 
    #print(val)
    #global cb
    #v = cb.get()
    
    str = val
    c.send(str.encode())
    #time.sleep(0.1)
    print ("N:",s.recv(1024).decode())
    

def takeSnapshot(event):
    
    global w
    global cb
    #print(cb.get())
    
    var="r "+cb.get()

    str1 = var
    c.send(str1.encode())
    v= int(c.recv(1024).decode())

    w.set(v)
    
    w.focus()

def moveup():
    str="u"
    c.send(str.encode())

def movedown():
    str="d"
    c.send(str.encode())

def moveleft():
    str="l"
    c.send(str.encode())

def moveright():
    str="r"
    c.send(str.encode())

def movestop():
    str="s"
    c.send(str.encode())


btn = tki.Button(root, text="Quit",bg="red",command=quit)
root.bind("q",quit)
btn.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

btn1 = tki.Button(root, text="Laser",bg="gray64",fg="blue",command=create_window1)
root.bind("l",create_window1)
btn1.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

btn2 = tki.Button(root, text="Gas",bg="gray64",fg="blue",command=create_window2)
root.bind("g",create_window2)
btn2.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

btn3 = tki.Button(root, text="Controler",bg="gray64",fg="blue")#,command=create_window3)
root.bind("c",create_window3)
btn3.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

v0=tki.IntVar()
v0.set(1)

w = tki.Scale(root, from_=0, to=300, orient= tki.HORIZONTAL ,command= print_value)
w.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
w.focus()


var = tki.StringVar()
#var.set("1")
data=("1", "2", "3", "4","5")


cb=Combobox(root, values=data,text="Motor",width="15",textvariable=var)
#cb.focus()
root.bind("<<ComboboxSelected>>",takeSnapshot)
cb.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

label = tki.Label(root,text = "Choose motor number")
label.pack(side="bottom")




root.title('RATAM')

#image()  #Display 
img = ImageTk.PhotoImage(Image.open("r5.jpg"))
panel = tki.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()  #Starts GUI
