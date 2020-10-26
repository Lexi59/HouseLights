from tkinter import *
import gpiozero as io
from time import sleep
import datetime
import tkinter.font as font
from functools import partial

#light class
class Light:
    def __init__(self, name, status, on , off):
        if on > 0:
            self.on = io.OutputDevice(on)
        else:
            self.on = 0
        if off > 0:
            self.off = io.OutputDevice(off)
        else:
            self.off = 0
        if status > 0:
            self.status = io.InputDevice(status)
        else:
            self.status = 0
        self.button = Button()
        self.name = name
        self.timerOn = ""
        self.timerOff = ""
        
#initialize GUI Window
window = Tk()
window.title("House Lights")
window.geometry('800x425')

#global variables
livingLights = []
familyLights = []
bedroomLights = []
garageLights = []
timerSettingMode = ""
settingTimerForLightNum = ""
myFont = font.Font(family = "Helvetica", size = 18)
myClockFont = font.Font(family = "Helvetica", size = 30)
currentDT = datetime.datetime.now()
mode = "normal"
currentPage = ""

clockLabel = Label(window, text = "%d:%d:%d" % (currentDT.hour, currentDT.minute, currentDT.second), font = myClockFont, compound = CENTER)
timerOnLabel = Label(window, text = "", font = myFont)
timerOffLabel = Label(window, text = "", font = myFont)
timerOnAmPmLabel = Label(window, text  = "", font = myFont)
timerOffAmPmLabel = Label(window, text = "", font = myFont)
livingButton = Button(window, text = "Living / Dining", font = myFont, fg='black',  activeforeground = 'black', height = 2, width = 40)
familyButton = Button(window, text = "Family Room / Entry", font = myFont, fg='black', activeforeground = 'black',height = 2, width = 40)
bedroomButton = Button(window, text = "Bedroom Area", font = myFont, fg='black',activeforeground = 'black',height = 2, width = 40)
garageButton = Button(window, text = "Garage / Exterior", font= myFont, fg='black', activeforeground = 'black',height = 2, width = 40)



#type Light info here
livingLightNames = ["1","2","3","4","5","6","7","8"]
livingOnPinNumbers = [0,0,0,0,0,0,0,0]
livingOffPinNumbers = [0,0,0,0,0,0,0,0]
livingStatusPinNumbers = [0,0,0,0,0,0,0,0]

familyLightNames = ["1","2","3","4","5"]
familyOnPinNumbers = [0,0,0,0,0]
familyOffPinNumbers = [0,0,0,0,0]
familyStatusPinNumbers = [0,0,0,0,0]

bedroomLightNames = ["1","2","3","4","5","6"]
bedroomOnPinNumbers = [17,0,0,0,0,0]
bedroomOffPinNumbers = [0,0,0,0,0,0]
bedroomStatusPinNumbers = [4,5,6,0,0,0]

garageLightNames = ["1","2","3","4"]
garageOnPinNumbers = [0,0,0,0]
garageOffPinNumbers = [0,0,0,0]
garageStatusPinNumbers = [0,0,0,0]

#create lights
for i in range(0, 8):
    livingLights.append(Light(livingLightNames[i],livingStatusPinNumbers[i],livingOnPinNumbers[i],livingOffPinNumbers[i]))
for i in range(0, 5):
    familyLights.append(Light(familyLightNames[i],familyStatusPinNumbers[i],familyOnPinNumbers[i],familyOffPinNumbers[i]))
for i in range(0, 6):
    bedroomLights.append(Light(bedroomLightNames[i], bedroomStatusPinNumbers[i],bedroomOnPinNumbers[i],bedroomOffPinNumbers[i]))
for i in range(0, 4):
    garageLights.append(Light(garageLightNames[i],garageStatusPinNumbers[i],garageOnPinNumbers[i],garageOffPinNumbers[i]))
    
#working functions
def clear():
    list = window.grid_slaves()
    for l in list:
        l.grid_forget()
        
def checkStatuses():
    global currentPage, mode
    colors = ["green","green","green","green"]
    if currentPage == "main":
        for i in range(0,8):
            if livingLights[i].status != 0 and livingLights[i].status.is_active:
                colors[0]="red"
        for i in range(0,5):
            if familyLights[i].status != 0 and familyLights[i].status.is_active:
                colors[1]="red"
        for i in range(0,6):
            if bedroomLights[i].status != 0 and bedroomLights[i].status.is_active:
                colors[2]="red"
        for i in range(0,4):
            if garageLights[i].status != 0 and garageLights[i].status.is_active:
                colors[3]="red"
        livingButton['bg'] = colors[0]
        livingButton['activebackground'] = colors[0]
        familyButton['bg'] = colors[1]
        familyButton['activebackground'] = colors[1]
        bedroomButton['bg'] = colors[2]
        bedroomButton['activebackground'] = colors[2]
        garageButton['bg'] = colors[3]
        garageButton['activebackground'] = colors[3]
    if currentPage == "living" and mode == "normal":
        for i in range(0,8):
            if livingLights[i].status != 0 and livingLights[i].status.is_active:
                livingLights[i].button['bg'] = 'red'
                livingLights[i].button['activebackground'] = 'red'
            else:
                livingLights[i].button['bg'] = 'green'
                livingLights[i].button['activebackground'] = 'green'
    if currentPage == "family" and mode == "normal":
        for i in range(0,5):
            if familyLights[i].status != 0 and familyLights[i].status.is_active:
                familyLights[i].button['bg'] = 'red'
                familyLights[i].button['activebackground'] = 'red'
            else:
                familyLights[i].button['bg'] = 'green'
                familyLights[i].button['activebackground'] = 'green'
    if currentPage == "bedroom"and mode == "normal":
        for i in range(0,6):
            if bedroomLights[i].status != 0 and bedroomLights[i].status.is_active:
                bedroomLights[i].button['bg'] = 'red'
                bedroomLights[i].button['activebackground'] = 'red'
            else:
                bedroomLights[i].button['bg'] = 'green'
                bedroomLights[i].button['activebackground'] = 'green'
    if currentPage == "garage"and mode == "normal":
        for i in range(0,4):
            if garageLights[i].status != 0 and garageLights[i].status.is_active:
                garageLights[i].button['bg'] = 'red'
                garageLights[i].button['activebackground'] = 'red'
            else:
                garageLights[i].button['bg'] = 'green'
                garageLights[i].button['activebackground'] = 'green'
def checkTimers():
    chour = datetime.datetime.now().hour
    cmin = datetime.datetime.now().minute
    if datetime.datetime.now().second >= 1:
        return
    for i in range(0,8):
        if livingLights[i].timerOn.split(":")[0] == "%2d"%chour and livingLights[i].timerOn.split(":")[1] == "%2d"%cmin and livingLights[i].on != 0:
            livingLights[i].on.on()
            sleep(.5)
            livingLights[i].on.off()
        if livingLights[i].timerOff.split(":")[0] == "%2d"%chour and livingLights[i].timerOff.split(":")[1] == "%2d"%cmin and livingLights[i].off != 0:
            livingLights[i].off.on()
            sleep(.5)
            livingLights[i].off.off()
    for i in range(0,5):
        if familyLights[i].timerOn.split(":")[0] == "%2d"%chour and familyLights[i].timerOn.split(":")[1] == "%2d"%cmin and familyLights[i].on != 0:
            familyLights[i].on.on()
            sleep(.5)
            familyLights[i].on.off()
        if familyLights[i].timerOff.split(":")[0] == "%2d"%chour and familyLights[i].timerOff.split(":")[1] == "%2d"%cmin and familyLights[i].off != 0:
            familyLights[i].off.on()
            sleep(.5)
            familyLights[i].off.off()
    for i in range(0,6):
        if bedroomLights[i].timerOn.split(":")[0] == "%2d"%chour and bedroomLights[i].timerOn.split(":")[1] == "%2d"%cmin and bedroomLights[i].on != 0:
            bedroomLights[i].on.on()
            sleep(.5)
            bedroomLights[i].on.off()
        if bedroomLights[i].timerOff.split(":")[0] == "%2d"%chour and bedroomLights[i].timerOff.split(":")[1] == "%2d"%cmin and bedroomLights[i].off != 0:
            bedroomLights[i].off.on()
            sleep(.5)
            bedroomLights[i].off.off()
    for i in range(0,4):
        if garageLights[i].timerOn.split(":")[0] == "%2d"%chour and garageLights[i].timerOn.split(":")[1] == "%2d"%cmin and garageLights[i].on != 0:
            garageLights[i].on.on()
            sleep(.5)
            garageLights[i].on.off()
        if garageLights[i].timerOff.split(":")[0] == "%2d"%chour and garageLights[i].timerOff.split(":")[1] == "%2d"%cmin and [i].off != 0:
            garageLights[i].off.on()
            sleep(.5)
            garageLights[i].off.off()
    
def tick():
    currentDT = datetime.datetime.now()
    clockLabel.config(text = "%02d:%02d:%02d" % (currentDT.hour, currentDT.minute, currentDT.second))
    checkStatuses()
    checkTimers()
    clockLabel.after(500, tick)
    
def changeTimerMode(mode):
    global timerSettingMode
    timerSettingMode = mode
    if mode == "on":
        timerOnButton['bg'] = 'blue'
        timerOnButton['activebackground'] = 'blue'
        timerOffButton['bg'] = '#94928e'
        timerOffButton['activebackground'] = '#94928e'
    if mode == "off":
        timerOffButton['bg'] = 'blue'
        timerOffButton['activebackground'] = 'blue'
        timerOnButton['bg'] = '#94928e'
        timerOnButton['activebackground'] = '#94928e'
        
def addNum(num):
    global timerSettingMode
    if timerSettingMode == "on":
        if len(timerOnLabel['text']) < 6:
            timerOnLabel['text'] += num
            timerOnLabel['text'] = timerOnLabel['text'].replace(":","")
            if len(timerOnLabel['text']) >= 2:
                timerOnLabel['text'] = timerOnLabel['text'][:-2] + ":" + timerOnLabel['text'][-2:]      
    else:
        if len(timerOffLabel['text']) < 6:
            timerOffLabel['text'] += num
            timerOffLabel['text'] = timerOffLabel['text'].replace(":","")
            if len(timerOffLabel['text']) >= 2:
                timerOffLabel['text'] = timerOffLabel['text'][:-2] + ":" + timerOffLabel['text'][-2:]

def addTime(time):
    global timerSettingMode
    if timerSettingMode == "on":
        timerOnAmPmLabel['text'] = time
    if timerSettingMode == "off":
        timerOffAmPmLabel['text'] = time
                            
def submitTimer():
    global currentPage, mode
    timerOn = timerOnLabel['text']
    timerOff = timerOffLabel['text']
    if timerOnAmPmLabel['text'] == "PM":
        newHour = int(timerOnLabel['text'].split(':')[0]) + 12
        timerOn = str(newHour)+":"+ timerOnLabel['text'].split(':')[1]
    if timerOffAmPmLabel['text'] == "PM":
        newHour = int(timerOffLabel['text'].split(':')[0]) + 12
        timerOff = str(newHour)+":"+ timerOffLabel['text'].split(':')[1]
    if currentPage == "bedroom" and settingTimerForLightNum >= 0:
        bedroomLights[settingTimerForLightNum].timerOn = timerOn
        bedroomLights[settingTimerForLightNum].timerOff = timerOff
        bedroomPage()
    if currentPage == "family" and settingTimerForLightNum >= 0:
        familyLights[settingTimerForLightNum].timerOn = timerOn
        familyLights[settingTimerForLightNum].timerOff = timerOff
        familyPage()
    if currentPage == "living" and settingTimerForLightNum >= 0:
        livingLights[settingTimerForLightNum].timerOn = timerOn
        livingLights[settingTimerForLightNum].timerOff = timerOff
        livingPage()
    if currentPage == "garage" and settingTimerForLightNum >= 0:
        garageLights[settingTimerForLightNum].timerOn = timerOn
        garageLights[settingTimerForLightNum].timerOff = timerOff
        garagePage()
    mode = "normal"
        
    
def delete():
    global timerSettingMode
    if timerSettingMode == "on":
        timerOnLabel['text'] = ""
        timerOnAmPmLabel['text'] = ""
    else:
        timerOffLabel['text'] = ""
        timerOffAmPmLabel['text'] = ""
        
def chooseLightSet():
    global currentPage, mode
    mode = "choosing"
    if currentPage == "bedroom":
        for i in range(0, len(bedroomLights)):
            bedroomLights[i].button['bg'] = 'yellow'
            bedroomLights[i].button['activebackground'] = 'yellow'  
    if currentPage == "living":
        for i in range(0, len(livingLights)):
            livingLights[i].button['bg'] = 'yellow'
            livingLights[i].button['activebackground'] = 'yellow'
            
    if currentPage == "family":
        for i in range(0, len(familyLights)):
            familyLights[i].button['bg'] = 'yellow'
            familyLights[i].button['activebackground'] = 'yellow'
            
    if currentPage == "garage":
        for i in range(0, len(garageLights)):
            garageLights[i].button['bg'] = 'yellow'
            garageLights[i].button['activebackground'] = 'yellow'
            
def chooseLightClear():
    global currentPage, mode
    mode = "choosing"
    if currentPage == "bedroom":
        for i in range(0, len(bedroomLights)):
            if bedroomLights[i].timerOn != "":
                bedroomLights[i].button['bg'] = 'yellow'
                bedroomLights[i].button['activebackground'] = 'yellow'
                bedroomLights[i].button['text'] = bedroomLights[i].timerOn + "-"+ bedroomLights[i].timerOff
    if currentPage == "living":
        for i in range(0, len(livingLights)):
            if livingLights[i].timerOn != "":
                livingLights[i].button['bg'] = 'yellow'
                livingLights[i].button['activebackground'] = 'yellow'
                livingLights[i].button['text'] = livingLights[i].timerOn + "-"+ livingLights[i].timerOff
    if currentPage == "family":
        for i in range(0, len(familyLights)):
            if familyLights[i].timerOn !="":
                familyLights[i].button['bg'] = 'yellow'
                familyLights[i].button['activebackground'] = 'yellow'
                familyLights[i].button['text'] = familyLights[i].timerOn + "-"+ familyLights[i].timerOff
    if currentPage == "garage":
        for i in range(0, len(garageLights)):
            if garageLights[i].timerOn != "":
                garageLights[i].button['bg'] = 'yellow'
                garageLights[i].button['activebackground'] = 'yellow'           
                garageLights[i].button['text'] = garageLights[i].timerOn + "-"+ garageLights[i].timerOff
def lightClicked(num):
    global mode, settingTimerForLightNum, currentPage
    if mode == "choosing":
        settingTimerForLightNum = num
        timerPage()
    if mode == "clear":
        mode = "normal"
        if currentPage == "bedroom":
            bedroomLights[num].timerOn = ""
            bedroomLights[num].timerOff = ""
        if currentPage == "living":
            livingLights[num].timerOn = ""
            livingLights[num].timerOff = ""
        if currentPage == "family":
            familyLights[num].timerOn = ""
            familyLights[num].timerOff = ""
        if currentPage == "garage":
            garageLights[num].timerOn = ""
            garageLights[num].timerOff = ""
        showTimers()
    if mode == "normal":
        if currentPage == "bedroom":
            if bedroomLights[num].status != 0:
                if bedroomLights[num].status.is_active and bedroomLights[num].off != 0:
                    bedroomLights[num].off.on()
                    sleep(.5)
                    bedroomLights[num].off.off()
                if bedroomLights[num].status.is_active == False and bedroomLights[num].on != 0:
                    bedroomLights[num].on.on()
                    sleep(.5)
                    bedroomLights[num].on.off()
        if currentPage == "living":
            if livingLights[num].status != 0:
                if livingLights[num].status.is_active and livingLights[num].off != 0:
                    livingLights[num].off.on()
                    sleep(.5)
                    livingLights[num].off.off()
                if livingLights[num].status.is_active == False and livingLights[num].on != 0:
                    livingLights[num].on.on()
                    sleep(.5)
                    livingLights[num].on.off()
        if currentPage == "family":
            if familyLights[num].status != 0:
                if familyLights[num].status.is_active and familyLights[num].off != 0:
                    familyLights[num].off.on()
                    sleep(.5)
                    familyLights[num].off.off()
                if familyLights[num].status.is_active == False and familyLights[num].on != 0:
                    familyLights[num].on.on()
                    sleep(.5)
                    familyLights[num].on.off()
        if currentPage == "garage":
            if garageLights[num].status != 0:
                if garageLights[num].status.is_active and garageLights[num].off != 0:
                    garageLights[num].off.on()
                    sleep(.5)
                    garageLights[num].off.off()
                if garageLights[num].status.is_active == False and garageLights[num].on != 0:
                    garageLights[num].on.on()
                    sleep(.5)
                    garageLights[num].on.off()
        
def showTimers():
    global currentPage, mode
    if currentPage == "bedroom":
        for i in range(0, len(bedroomLights)):
            if bedroomLights[i].button['bg'] != '#94928e':
                bedroomLights[i].button['bg'] = '#94928e'
                bedroomLights[i].button['activebackground'] = '#94928e'
                bedroomLights[i].button['text'] = bedroomLights[i].timerOn + "-" + bedroomLights[i].timerOff
                mode = "show"
            else:
                bedroomLights[i].button['bg'] = 'red'
                bedroomLights[i].button['activebackground'] = 'red'
                bedroomLights[i].button['text'] = bedroomLights[i].name
                mode = "normal"
    if currentPage == "living":
        for i in range(0, len(livingLights)):
            if livingLights[i].button['bg'] != '#94928e':
                livingLights[i].button['bg'] = '#94928e'
                livingLights[i].button['activebackground'] = '#94928e'
                livingLights[i].button['text'] = livingLights[i].timerOn + "-" + livingLights[i].timerOff
                mode = "show"
            else:
                livingLights[i].button['bg'] = 'red'
                livingLights[i].button['activebackground'] = 'red'
                livingLights[i].button['text'] = livingLights[i].name
                mode = "normal"
    if currentPage == "family":
        for i in range(0, len(familyLights)):
            if familyLights[i].button['bg'] != '#94928e':
                familyLights[i].button['bg'] = '#94928e'
                familyLights[i].button['activebackground'] = '#94928e'
                familyLights[i].button['text'] = familyLights[i].timerOn + "-" + familyLights[i].timerOff
                mode = "show"
            else:
                familyLights[i].button['bg'] = 'red'
                familyLights[i].button['activebackground'] = 'red'
                familyLights[i].button['text'] = familyLights[i].name
                mode = "normal"
    if currentPage == "garage":
        for i in range(0, len(garageLights)):
            if garageLights[i].button['bg'] != '#94928e':
                garageLights[i].button['bg'] = '#94928e'
                garageLights[i].button['activebackground'] = '#94928e'
                garageLights[i].button['text'] = garageLights[i].timerOn + "-" + garageLights[i].timerOff
                mode = "show"
            else:
                garageLights[i].button['bg'] = 'red'
                garageLights[i].button['activebackground'] = 'red'
                garageLights[i].button['text'] = garageLights[i].name
                mode = "normal"
def clearAllTimers():
    global currentPage
    if currentPage == "bedroom":
        for i in range(0,len(bedroomLights)):
            bedroomLights[i].timerOn = ""
            bedroomLights[i].timerOff = ""
    if currentPage == "living":
        for i in range(0,len(livingLights)):
            livingLights[i].timerOn = ""
            livingLights[i].timerOff = ""
    if currentPage == "family":
        for i in range(0,len(familyLights)):
            familyLights[i].timerOn = ""
            familyLights[i].timerOff = ""
    if currentPage == "garage":
        for i in range(0,len(garageLights)):
            garageLights[i].timerOn = ""
            garageLights[i].timerOff = ""
    showTimers()
    
def clearTimer():
    global mode
    chooseLightClear()
    mode = "clear"
        
#global widgets
timerOnButton = Button(window, text = "Time On:", command = partial(changeTimerMode, "on"), font = myFont, bg = '#94928e', fg = 'white', activebackground = '#94928e', activeforeground = 'white')
timerOffButton = Button(window, text = "Time Off:", command = partial(changeTimerMode, "off"), font = myFont, bg = '#94928e', fg = 'white', activebackground = '#94928e', activeforeground = 'white')
timerSetButton = Button(window, text = "Timer Set", command = chooseLightSet, font= myFont, bg='blue', fg='white',activebackground = 'blue', activeforeground = 'white',height = 2, width = 12)
clearTimerButton = Button(window, text = "Clear Timer", command = clearTimer, font= myFont, bg='blue', fg='white',activebackground = 'blue', activeforeground = 'white',height = 2, width = 12)
showTimersButton = Button(window, text = "Show Timers", command = showTimers, font= myFont, bg='blue', fg='white',activebackground = 'blue', activeforeground = 'white',height = 2, width = 12)
clearAllTimersButton = Button(window, text = "Clear All", command = clearAllTimers, font= myFont, bg='blue', fg='white',activebackground = 'blue', activeforeground = 'white',height = 2, width = 12)
 
#paging functions
def mainPage():
    global currentPage
    clear()
    currentPage = "main"
    checkStatuses()
    clockLabel.grid(column = 0, row = 0, columnspan = 4)
    livingButton.grid(column = 0, row = 1, padx = 3, pady = 4)
    livingButton['command'] = livingPage
    familyButton.grid(column = 0, row = 2, padx = 3, pady = 4)
    familyButton['command'] = familyPage
    bedroomButton.grid(column = 0, row = 3, padx = 3, pady = 4)
    bedroomButton['command'] = bedroomPage
    garageButton.grid(column = 0, row = 4, padx = 3, pady = 4)
    garageButton['command'] = garagePage
    Button(window, text = "All On", font= myFont, bg='red', fg='black',activebackground = 'red', activeforeground = 'black', highlightthickness = 3, highlightbackground = 'black', height = 4, width = 15).grid(column = 2, row = 1, rowspan =2, padx = 3, pady = 4)
    Button(window, text = "All Off", font= myFont, bg='green', fg='black',activebackground = 'green', activeforeground = 'black',highlightthickness = 3, highlightbackground = 'black',height = 4, width = 15).grid(column = 2, row = 3, rowspan =2, padx = 3, pady = 4)

mainPageButton = Button(window, text = "<-", command = mainPage, bg= 'white', fg= 'black', height = 2, width = 2)

def timerPage():
    clear()
    mainPageButton.grid(column = 0, row = 0, sticky=W)
    clockLabel.grid(column = 1, row = 0, columnspan = 2)
    
    Button(window, text = "1", command = partial(addNum, "1"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 0, row = 1, padx = 3, pady = 4)
    Button(window, text = "2", command = partial(addNum, "2"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 1, row = 1, padx = 3, pady = 4)
    Button(window, text = "3", command = partial(addNum, "3"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 2, row = 1, padx = 3, pady = 4)
    Button(window, text = "4", command = partial(addNum, "4"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 0, row = 2, padx = 3, pady = 4)
    Button(window, text = "5", command = partial(addNum, "5"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 1, row = 2, padx = 3, pady = 4)
    Button(window, text = "6", command = partial(addNum, "6"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 2, row = 2, padx = 3, pady = 4)
    Button(window, text = "7", command = partial(addNum, "7"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 0, row = 3, padx = 3, pady = 4)
    Button(window, text = "8", command = partial(addNum, "8"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 1, row = 3, padx = 3, pady = 4)
    Button(window, text = "9", command = partial(addNum, "9"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 2, row = 3, padx = 3, pady = 4)
    Button(window, text = "AM", command = partial(addTime, "AM"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 0, row = 4, padx = 3, pady = 4)
    Button(window, text = "0", command = partial(addNum, "0"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 1, row = 4, padx = 3, pady = 4)
    Button(window, text = "PM", command = partial(addTime, "PM"), font= myFont, bg='#94928e', fg='white',activebackground = '#94928e', activeforeground = 'white',height = 2, width = 10).grid(column = 2, row = 4, padx = 3, pady = 4)
    
    timerOnButton.grid(row=1, column = 3)
    timerOnLabel.grid(row = 1, column = 4)
    timerOnAmPmLabel.grid(row = 1, column = 5)
    timerOffButton.grid(row = 2, column = 3)
    timerOffLabel.grid(row = 2, column = 4)
    timerOffAmPmLabel.grid(row = 2, column = 5)
    
    Button(window, text = "OK", command = submitTimer, font = myFont, bg = '#94928e', fg = 'white', activebackground = '#94928e', activeforeground = 'white', height = 1).grid(row = 3, column = 4)
    Button(window, text = "Del", command = delete, font = myFont, bg = '#94928e', fg = 'white', activebackground = '#94928e', activeforeground = 'white', height = 1).grid(row = 3, column = 3)
    
def bedroomPage():
    global currentPage
    clear()
    currentPage = "bedroom"
    checkStatuses()
    mainPageButton.grid(column = 0, row = 0, sticky = W)
    clockLabel.grid(column = 1, row = 0, columnspan = 2)
    for i in range(0,6):
        bedroomLights[i].button = Button(window, text = bedroomLights[i].name, command = partial(lightClicked, i), font= myFont, fg='black', activeforeground = 'black',height = 2, width = 12)
    
    counter = 0
    for r in range(1,5):
        for c in range(0,3):
            if counter < 6:
                bedroomLights[(r-1)*3+c].button.grid(column = c, row = r, padx = 3, pady=4)
                counter+=1
    
    timerSetButton.grid(column = 3, row = 1, padx = 6, pady = 4)
    clearTimerButton.grid(column = 3, row = 2, padx = 6, pady = 4)
    showTimersButton.grid(column = 3, row = 3, padx = 7, pady = 4)
    clearAllTimersButton.grid(column = 3, row = 4, padx = 10, pady = 4)
    
    
def livingPage():
    global currentPage
    clear()
    currentPage = "living"
    checkStatuses()
    mainPageButton.grid(column = 0, row = 0, sticky = W)
    clockLabel.grid(column = 1, row = 0, columnspan = 2)
    
    for i in range(0,8):
        livingLights[i].button = Button(window, text = livingLights[i].name, command = partial(lightClicked, i), font= myFont, fg='black', activeforeground = 'black',height = 2, width = 12)
    
    counter = 0
    for r in range(1,5):
        for c in range(0,3):
            if counter < 8:
                livingLights[(r-1)*3+c].button.grid(column = c, row = r, padx = 3, pady=4)
                counter+=1
        
    timerSetButton.grid(column = 3, row = 1, padx = 6, pady = 4)
    clearTimerButton.grid(column = 3, row = 2, padx = 6, pady = 4)
    showTimersButton.grid(column = 3, row = 3, padx = 7, pady = 4)
    clearAllTimersButton.grid(column = 3, row = 4, padx = 10, pady = 4)
    
def familyPage():
    global currentPage
    clear()
    currentPage = "family"
    checkStatuses()
    mainPageButton.grid(column = 0, row = 0, sticky = W)
    clockLabel.grid(column = 1, row = 0, columnspan = 2)
    
    for i in range(0,5):
        familyLights[i].button = Button(window, text = familyLights[i].name, command = partial(lightClicked, i), font= myFont, fg='black', activeforeground = 'black',height = 2, width = 12)
    
    counter = 0
    for r in range(1,5):
        for c in range(0,3):
            if counter < 5:
                familyLights[(r-1)*3+c].button.grid(column = c, row = r, padx = 3, pady=4)
                counter+=1
        
    timerSetButton.grid(column = 3, row = 1, padx = 6, pady = 4)
    clearTimerButton.grid(column = 3, row = 2, padx = 6, pady = 4)
    showTimersButton.grid(column = 3, row = 3, padx = 7, pady = 4)
    clearAllTimersButton.grid(column = 3, row = 4, padx = 10, pady = 4)
    
def garagePage():
    global currentPage
    clear()
    currentPage = "garage"
    checkStatuses()
    mainPageButton.grid(column = 0, row = 0, sticky = W)
    clockLabel.grid(column = 1, row = 0, columnspan = 2)
    
    for i in range(0,4):
        garageLights[i].button = Button(window, text = garageLights[i].name, command = partial(lightClicked, i), font= myFont, fg='black', activeforeground = 'black',height = 2, width = 12)
    
    counter = 0
    for r in range(1,5):
        for c in range(0,3):
            if counter < 4:
                garageLights[(r-1)*3+c].button.grid(column = c, row = r, padx = 3, pady=4)
                counter+=1
        
    timerSetButton.grid(column = 3, row = 1, padx = 6, pady = 4)
    clearTimerButton.grid(column = 3, row = 2, padx = 6, pady = 4)
    showTimersButton.grid(column = 3, row = 3, padx = 7, pady = 4)
    clearAllTimersButton.grid(column = 3, row = 4, padx = 10, pady = 4)

mainPage()
changeTimerMode("on")
tick()
window.mainloop()