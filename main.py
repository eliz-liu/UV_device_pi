#!/usr/bin/python
# -*- coding:UTF-8 -*-


from Tkinter import *
import ttk
import threading
import time as timer
import Si1145 as Sensor
from tkFont import Font
from datetime import *
import tkMessageBox

#globals

UVindex = ""
gui = Tk()
gui.title("UV Index")
UVdate= ""
UVcategory = ["low","moderate","high","very high","extreme"]
UVlist=[]
UVdict={}


# Bell function
def bell():
    # call bell method
    gui.bell()

def get_UVcategory(UVindex):
    global UVcategory
    if UVindex >= 0 and UVindex <= 2:
        return UVcategory[0]
    elif UVindex > 2 and UVindex <= 5:
        return UVcategory[1]
    elif UVindex > 5 and UVindex <= 7:
        return UVcategory[2]
    elif UVindex > 7 and UVindex <= 10:
        return UVcategory[3]
    elif UVindex > 10:
        return UVcategory[4]

def ShowResults():
    UVlog = open("MyUVlog.txt","r+") 
    UVread = UVlog.read().splitlines()

    #convert list to dict
    for i in range(0,len(UVread)):
        print(UVread[i].split("|"))
        UVlist.append(UVread[i].split("|"))
    
    for i in range(0,len(UVlist)):
        UVdate = UVlist[i][0]
        UVIndex = UVlist[i][1]
        UVdict[UVdate] = UVIndex
    
    #max UV index
    MaxUVIndex = max(UVdict.values())

    
    #min UV index
    MinUVIndex = min(UVdict.values())

    #get max length
    UVdate = list(UVdict.keys())
    UVIndex = list(UVdict.values())

    last_record = max(index for index, item in enumerate(UVIndex) if item == MaxUVIndex)
    first_record = UVIndex.index(MaxUVIndex)
    
    UVlength = datetime.strptime(UVdate[last_record], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(UVdate[first_record], '%Y-%m-%d %H:%M:%S.%f')


    last_date = datetime.strptime(UVdate[-1],'%Y-%m-%d %H:%M:%S.%f')

    first_date = datetime.strptime(UVdate[0],'%Y-%m-%d %H:%M:%S.%f')

    #Message Box
    tkMessageBox.showinfo("Results from %s to %s" %(first_date,last_date), "Max UV Index detected: %s\nMin UV Index detected: %s\nLength of Max UV Index detected : %s" %(MaxUVIndex,MinUVIndex,UVlength))


#get data/save data thread

def get_data():
    global UVindex
    global UVdate
    Sensor.Si1145_Init()
    try:
        while True:

            #get UV index and time
            UVindex = Sensor.Si1145_readUV()
            UVindex /= 100.0
            UVdate = datetime.now()

            print "UV: ", UVindex, UVdate #shows in CLI UV index and time

            #saves UV index and time
            UVlog = open("MyUVlog.txt","a+")
            UVlog.write(str(UVdate)+"|"+str(UVindex))
            UVlog.write("\n")
            UVlog.close()
 
            timer.sleep(1)

    except:
        Sensor.Si1145_close()
            
def update_gui():
    #update
    print "update_gui: ", UVindex, datetime.now()
    try:
        while True:
            if UVindex:

                #change index
                lblUVindex.config(text="")
                lblUVindex.config(text= UVindex)

                #change date
                lblDate.config(text="")
                UVdateString = UVdate.strftime("%d/%m/%Y %H:%M:%S")
                lblDate.config(text=UVdateString)

                #show alert
                if lblUVlevel['text'] != get_UVcategory(UVindex):
                    bell()
                    tkMessageBox.showwarning("UV index Warning!", "New %s UV index levels detected!" %get_UVcategory(UVindex))
                    
                
                #change UV index level
                lblUVlevel.config(text="")
                lblUVlevel.config(text=get_UVcategory(UVindex))

            timer.sleep(1)
    except:
        print "no"



def read_data():
    t1 = threading.Thread(target = get_data)
    t1.daemon = True
    t1.start()
    

if __name__ == "__main__":
    
    #window layout
    gui.geometry("300x300")
    frameTop = Frame(gui)
    frameTop.pack(side=TOP)
    fontStyle1 = Font(family="MS Reference Sans Serif",size= 15)

    #lblUVDate
    lblDate = Label(frameTop)
    lblDate.pack(fill="both", side="left")
    lblempty = Label(frameTop, text = "", font=fontStyle1)
    lblempty.pack(fill="both", side="left")
    
    #lblUVindex
    fontStyle = Font(family="MS Reference Sans Serif",size=50)
    lblUVindex = Label(gui, font=fontStyle)
    lblUVindex.pack(expand=True)

    #lblUVlevel
    lblUVlevel = Label(gui, font=fontStyle1)
    lblUVlevel.pack(expand=True)

    resultsBtn = Button(gui,text="Show UV Results", command=ShowResults)

    resultsBtn.pack()
    

    #treading read_data    
    read_data()

    #treading update_gui
    t = threading.Thread(target = update_gui)
    t.daemon = True
    t.start()
    
    #mainloop
    gui.mainloop()
