"""
Code by: Paolo Decena
If you need to contact me, or stab me in the face because I am the best codemonkey,
you can reach me at paolo.decena@gmail.com

****This is Python2 code. Run in linux using python2 command*****

You need to make sure RPi.GPIO 0.5.5 is installed. Either method should work:

    wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.5.tar.gz
    tar -zxf RPI.GPIO-0.5.5.tar.gz
    cd RPi.GPIO-0.5.5
    sudo python setup.py install

    or

    sudo apt-get install update
    sudo apt-get install python-dev
    sudo apt-get install python-rpi.gpio
    sudo apt-get install python-imaging

"""

from Tkinter import *
from PIL import Image, ImageTk
import time   ##exactly what it sounds like

"""
## GPIO specific lines setting up the GPIO on the pi

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)   ##BCM numbering system

## setup GPIO pins as output to send START and STOP signals to MCU

GPIO.setup(23, GPIO.OUT)  ##pin 23 intended as start signal pin
GPIO.output(23, FALSE)
GPIO.setup(24, GPIO.OUT)  ##pin 24 intended as stop signal pin
GPIO.output(24, FALSE)
GPIO.setup(25, GPIO.IN)
GPIO.add_event_detect(25,GPIO.RISING,bouncetime=750)
"""

## defining global variables
lastRunCount=0
batchNumber=0
verified=0
root=0
delay=0

## defining popup login window
class loginWindow(object):
    def __init__(self,master):
        self.value='N/A'

        top=self.top=Toplevel(master)
        self.l=Label(top,text='Debugger/Admin Login')
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
        self.c=Button(top,text='Batch Finished',command=self.inc)
        self.c.pack()

        if self.value == 'pi':
            global verified
            verified=1

    def inc(self):
        global batchNumber
        batchNumber = batchNumber +1

    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

## defining the main window
class mainWindow(object):
    def __init__(self,master):
        self.master=master

        ## defining the frame everything goes in
        self.mainframe=Frame(master)
        self.mainframe.grid(column=1,row=1,sticky=N+W+E+S)

        ## defining spacing frames
        self.leftframe=Frame(master,width=115)
        self.leftframe.grid(column=0,row=0,columnspan=1,sticky=N+W+E+S)
        self.rightframe=Frame(master,width=115)
        self.rightframe.grid(column=10,row=0,columnspan=1,sticky=N+W+E+S)
        self.topframe=Frame(master,height=25)
        self.topframe.grid(column=0,row=0,sticky=N+W+E+S)
        self.bottomframe=Frame(master,height=75)
        self.bottomframe.grid(column=0,row=10,sticky=N+W+E+S)

        # background
        self.bgImage=Image.open("GUIbg.jpg")
        self.bgPhoto=ImageTk.PhotoImage(self.bgImage)
        self.bg=Label(master,image=self.bgPhoto)
        self.bg.place(x=0,y=0,relwidth=1,relheight=1)

        ## defining buttons and other widgets
        # machine state display
       # self.statusImage=Image.open("Label-MachineStatus.jpg")
       # self.statusPhoto=ImageTk.PhotoImage(self.statusImage)
        self.statusLabel=Label(master,text='Machine Status')
        self.statusLabel.grid(column=2,row=4,sticky=N+W+E+S)
        self.status=Entry(master)
        self.status.grid(column=2,row=5,sticky=W+E,padx=50)
        self.status.insert(0,"Machine Status Here")
        
        # throughput display
        self.batchLabel=Label(master,text='Number of Batches Complete')
        self.batchLabel.grid(column=2,row=6,sticky=N+W+E+S)
        self.batchCounter=Entry(master)
        self.batchCounter.grid(column=2,row=7,sticky=W+E,padx=50)
        self.batchCounter.insert(0,batchNumber)
        
        # previous run display
        self.prevLabel=Label(master,text='Batches Completed Before Reset')
        self.prevLabel.grid(column=2,row=8,sticky=N+W+E+S)
        self.lastRunDisp=Entry(master)
        self.lastRunDisp.grid(column=2,row=9,sticky=W+E,padx=50)
        self.lastRunDisp.insert(0,lastRunCount)

        # hortitech logo
        #self.logoImage=Image.open("logo.jpg")
        #self.logoPhoto=ImageTk.PhotoImage(self.logoImage)
        #self.logo=Label(master,image=self.logoPhoto)
        #self.logo.grid(column=2,row=1,rowspan=3,sticky=N+W+E+S)

        # start button
        self.startImage=Image.open("Button-Start.jpg")
        self.startPhoto=ImageTk.PhotoImage(self.startImage)
        self.startB=Button(master,text='Start',command=self.start,image=self.startPhoto)
        self.startB.grid(column=1,row=1,sticky=W+E,pady=5)

        # stop button
        self.stopImage=Image.open("Button-Halt.jpg")
        self.stopPhoto=ImageTk.PhotoImage(self.stopImage)
        self.stopB=Button(master,text='Stop',command=self.stop,image=self.stopPhoto)
        self.stopB.grid(column=1,row=2,sticky=W+E,pady=5)

        # close button
        self.closeImage=Image.open("Button-Close.jpg")
        self.closePhoto=ImageTk.PhotoImage(self.closeImage)
        self.closeB=Button(master,text='Close',command=self.close,image=self.closePhoto)
        self.closeB.grid(column=3,row=1,sticky=W+E,pady=5)

        # step button
        self.stepImage=Image.open("Button-StepInto.jpg")
        self.stepPhoto=ImageTk.PhotoImage(self.stepImage)
        self.stepB=Button(master,text='Step',command=self.step,image=self.stepPhoto)
        self.stepB.grid(column=1,row=3,sticky=W+E,pady=5)

        # reset button
        self.resetImage=Image.open("Button-Reset.jpg")
        self.resetPhoto=ImageTk.PhotoImage(self.resetImage)
        self.resetB=Button(master,text='Reset',command=self.reset,image=self.resetPhoto)
        self.resetB.grid(column=3,row=3,sticky=W+E,pady=5)

        # suspend button
        #self.suspendB=Button(master,text='Suspend',command=self.suspendToggle)
        #self.suspendB.grid(column=1,row=4,sticky=W+E,pady=5)

        # clean button
        #self.cleanB=Button(master,text='Clean')
        #self.cleanB.grid(column=3,row=4,sticky=W+E,padx=5)

        # batch increase button
        #self.testB=Button(master,text='Batch Finished',command=self.batchFinished,state=DISABLED)
        #self.testB.grid(column=3,row=2,sticky=W+E,pady=5)
        #if verified==1:
        #    self.testB.config(state=NORMAL)

        # Master Menu Bar Setup
        menubar = Menu(master)
        master.config(menu=menubar)

        # Menu for admin/debugger mode
        #modeMenu=Menu(menubar)
        #modeMenu.add_command(label="Switch Operating Mode", command=self.loginPopup)
        #menubar.add_cascade(label="Mode",menu=modeMenu)

    def start(self):
        self.status.delete(0,END)
        self.status.insert(0,"Starting")
##        GPIO.output(24,FALSE)
       # GPIO.output(23,TRUE)  #contrary to the online tutorial i was following, true sends a high on the pin

    def stop(self):
        self.status.delete(0,END)
        self.status.insert(0,"Stopping")
       # GPIO.output(23,FALSE)
       # GPIO.output(24,TRUE)
        global delay
        while delay!=25:
            delay=delay+1;
       # GPIO.output(24,FALSE)
        delay=0

    def close(self):
        root.destroy()

    def step(self):
        self.status.delete(0,END)
        self.status.insert(0,"Stepped")

    def batchIncrease(self):
        global batchNumber
        batchNumber=batchNumber+1
        self.batchCounter.delete(0,END)
        self.batchCounter.insert(0,batchNumber)

    def reset(self):
        global batchNumber
        global lastRunCount
        self.stop()
        lastRunCount=batchNumber
        batchNumber=0
        self.batchCounter.delete(0,END)
        self.batchCounter.insert(0,batchNumber)
        self.lastRunDisp.delete(0,END)
        self.lastRunDisp.insert(0,lastRunCount)
        self.status.delete(0,END)
        self.status.insert(0,"Batch Counter Was Reset")

    def suspendToggle(self):
        if self.suspendB.config('text')[-1] == 'Suspend':
            self.suspendB.config(text='Resume')
        else:
            self.suspendB.config(text='Suspend')

    def loginPopup(self):
        self.w=loginWindow(self.master)
        self.master.wait_window(self.w.top)

    def entryCheck(self):
       return self.w.value

def refresh():
    #print "%d" % batchNumber
    if GPIO.event_detected(25):
        m.batchIncrease()
    if batchNumber==5:
        m.stop()
    root.after(25,refresh)


if __name__ == "__main__":
    global root
    root=Tk()
    m=mainWindow(root)
        #if verified == 1:
    #        mainWindow.testB.config(state=NORMAL)
    #        m=mainWindow(root)
    root.after(25,refresh)
    root.mainloop()
