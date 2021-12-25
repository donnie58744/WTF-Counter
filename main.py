# Created by the best duo Donovan and Erik Whysong

import json
import threading
from tkinter.constants import CENTER, END
import sys
import os
import csv
import random
from datetime import date
from datetime import datetime
from threading import Timer
from PIL import Image, ImageTk
from itertools import count
from time import sleep

try:
    import tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root, top
    root = tk.Tk()
    top = mainWindow (root)
    root.mainloop()

w = None
def create_mainWindow(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
    Correct form of call: 'create_mainWindow(root, *args, **kwargs)' .'''
    global w, w_win, root, top
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = mainWindow (w)
    return (w, top)

def destroy_mainWindow():
    global w
    w.destroy()
    w = None

usersFile = 'data.json'
userArray = []
dateArray=[]
gifCheck = 1
gif = None
gifTimer = 5
gifArray = []
compareToday = ''
updateTimer = 10.0

# Only took me 5 fucking hours to find this and make it work but this displays GIFs! (Shout out to https://stackoverflow.com/a/43770948/13276597)
class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
            print(self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None
        self.delay = 0
        self.loc = 0

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

class mainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
        top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        width= top.winfo_screenwidth() 
        height= top.winfo_screenheight()
        #setting tkinter window size
        top.geometry("%dx%d" % (width, height))
        #top.attributes('-fullscreen', True)
        top.minsize(750, 650)
        top.resizable(1,  1)
        top.title("What The FUCK! Counter")
        top.configure(background="#5e5e5e")

        self.createUserBtn = tk.Button(top,fg='#4fed3e', borderwidth=2, bg='#080808', background='#080808')
        self.createUserBtn.place(relx=0.032, rely=0.022, height=38, width=97)
        self.createUserBtn.configure(command=self.createUser)
        self.createUserBtn.configure(highlightbackground="black")
        self.createUserBtn.configure(text='''Create User''')

        self.usernameEntry = tk.Entry(top)
        self.usernameEntry.configure(background="white")
        self.usernameEntry.configure(cursor="fleur")
        self.usernameEntry.configure(font="TkFixedFont")
        self.usernameEntry.configure(foreground="#000000")
        self.usernameEntry.configure(insertbackground="black")
        self.usernameEntry.configure(justify='center')

        self.usernameLabel = tk.Label(top)
        self.usernameLabel.configure(background="#5e5e5e")
        self.usernameLabel.configure(foreground="#000000")
        self.usernameLabel.configure(text='''Username:''')

        self.passwordEntry = tk.Entry(top)
        self.passwordEntry.configure(background="white")
        self.passwordEntry.configure(font="TkFixedFont")
        self.passwordEntry.configure(foreground="#000000")
        self.passwordEntry.configure(insertbackground="black")

        self.passwordLabel = tk.Label(top)
        self.passwordLabel.configure(background="#5e5e5e")
        self.passwordLabel.configure(foreground="#000000")
        self.passwordLabel.configure(text='''Pin (4 digits):''')

        self.closeBtn = tk.Button(top)
        self.closeBtn.configure(command=self.closeUserMenu)
        self.closeBtn.configure(activebackground="#5e5e5e")
        self.closeBtn.configure(activeforeground="#5e5e5e")
        self.closeBtn.configure(background="#5e5e5e")
        self.closeBtn.configure(foreground="#000000")
        self.closeBtn.configure(highlightbackground="#5e5e5e")
        self.closeBtn.configure(highlightcolor="black")
        self.closeBtn.configure(text='''X''')

        self.wtfBtn = tk.Button(top,borderwidth=0,foreground='black')
        self.wtfBtn.place(relx=0.8, rely=0.733, height=28, width=77, anchor=CENTER)
        self.wtfBtn.configure(text='''WTF''')
        self.wtfBtn.configure(command=self.counter)

        self.wtfTitleLabel = tk.Label(top)
        self.wtfTitleLabel.place(relx=0.5, rely=0.12, height=55, width=600, anchor=CENTER)
        self.wtfTitleLabel.configure(background="#5e5e5e")
        self.wtfTitleLabel.configure(font="-family {Phosphate} -size 48")
        self.wtfTitleLabel.configure(foreground="#000000")
        self.wtfTitleLabel.configure(text='''What The Fuck!''')

        self.wtfCounterLabel = tk.Label(top)
        self.wtfCounterLabel.place(relx=0.5, rely=0.25, height=33, width=105, anchor=CENTER)
        self.wtfCounterLabel.configure(activebackground="#f9f9f9")
        self.wtfCounterLabel.configure(activeforeground="black")
        self.wtfCounterLabel.configure(background="#5e5e5e")
        self.wtfCounterLabel.configure(font="-family {Academy Engraved LET} -size 30")
        self.wtfCounterLabel.configure(foreground="#000000")
        self.wtfCounterLabel.configure(highlightbackground="#d9d9d9")
        self.wtfCounterLabel.configure(highlightcolor="black")
        self.wtfCounterLabel.configure(text=self.getCounter())

        # Load
        global compareToday
        global gif
        gif = ImageLabel(root)
        compareToday = (date.today()).strftime("%m/%d/%y")
        
        self.setupGifs()
        self.dailyReset()

    # This checks to see if the csv file is empty
    def initCsv(self):
        with open('counterLog.csv', 'r',) as file:
            counterLogReader = csv.reader(file, delimiter = ',')
            for row in counterLogReader:
                if (row[0]=='date' and row[1] ==  'time'):
                    return True
                else:
                    return False
            else:
                print("empty")
                return False

    def writeCsv(self):
        today = (date.today()).strftime("%m/%d/%y")
        currentTime = (datetime.now()).strftime("%H:%M:%S")

        with open('counterLog.csv', mode='a') as counterLogFile:
            counterLogWritter = csv.writer(counterLogFile, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            if (self.initCsv() == False):
                
                counterLogWritter.writerow(['date', 'time'])
                counterLogWritter.writerow([today, currentTime])
            else:
                counterLogWritter.writerow([today, currentTime])

    def logCounter(self):
        global dateArray

        today = (date.today()).strftime("%m/%d/%y")
        currentTime = (datetime.now()).strftime("%H:%M:%S")

        with open(usersFile,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Get dates from json
            for row in file_data['dates']:
                # Add dates to array
                dateArray.append(row['date'])
                
                # Check if todays date is in the dates array / If not then add a new dir in json
                if (today in dateArray):
                    if (row['date'] == today):
                        row['time'] += '|'+currentTime+'|-'
                else:
                    # Check if array is finished searching
                    if (len(dateArray) == len(file_data['dates'])):
                        # Create New Date Entry
                        a_dict = {'date':today, 'time':''}

                        # Join new_data with file_data inside emp_details
                        file_data["dates"].append(a_dict)
                        
                        print('No date entry found. Creating one now...')

            # Reset vars
            dateArray=[]

            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            file.truncate()

    def counterUser(self, username, password):
        with open(usersFile,'r+') as file:
            data = json.load(file)

            for row in data['users']: 
                if (username == row['username'] and password == row['password']):
                    # add to wtf counter and to users profile
                    row['wtf']+=1

            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(data, file, indent = 4)
            file.truncate()

    def achivements(self):
        # load json file
        with open(usersFile,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Get wtf counter
            for row in file_data['acheivements']:
                if (self.getCounter() == row['value']):
                    print(row['name'])

    def getCounter(self):
        with open(usersFile,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Get wtf counter
            for row in file_data['wtfCounter']:
                return row['counter']

    def dailyReset(self):
        global compareToday
        global updateTimer

        # Start thread
        thread = Timer(updateTimer,self.dailyReset)

        if (thread.is_alive()):
            print('Restart Timer')
            thread.cancel()
        thread.daemon = True
        thread.start()
        today = (date.today()).strftime("%m/%d/%y")

        # If the day changes then reset wtf counter
        if (compareToday != today):
            # Set the date compare var to today
            compareToday = today
            with open(usersFile,'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                
                # Reset global wtf counter
                for row in file_data['wtfCounter']:
                    row["counter"] = 0
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
                file.truncate()

                # Refresh counter
                self.setCounter()

            print('Good Morning! WTF Counter has been reset')


    def clearGif(self):
        global gif
        global gifCheck
        gif.unload()
        gif.place_forget()
        # Wait a lil bit to prevent GIF bullshit
        sleep(0.2)
        gifCheck = True

    def setupGifs(self):
        global gifArray
        for filename in os.listdir('gifs/'):
            if not filename.startswith('.') and os.path.isfile(os.path.join('gifs/', filename)):
                gifArray.append(filename)
        
          
    def randomGif(self):  
        global gifArray
        global gifCheck
        global gif

        print(gifArray)
        
        # gif check is so you dont have multiple gifs at once
        if (gifCheck):
            randomGifFile = random.choice(gifArray)

            gif.place(relx=0.5, rely=0.7, anchor=CENTER)
            gif.load('gifs/'+randomGifFile)

            t = Timer(gifTimer, self.clearGif)
            t.daemon = True
            t.start()
        gifCheck = False

    def createUser(self, filename=usersFile):
        global userArray
        
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        # Menu toggle
        if (self.usernameEntry.winfo_viewable() == 0):
            self.showUserMenu()

        else:
            with open(filename,'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                
                if (username == '' or password == ''):
                    print('Username and Password is required')
                else:
                    for users in file_data['users']:
                        userArray.append(users['username'])
                        
                        if (len(userArray) == len(file_data['users'])):
                            
                            if (username in userArray):
                                print('User Exists')
                            else:
                                print('Creating User...')
                                a_dict = {'username':username, 'password':password, 'wtf':0}

                                # Join new_data with file_data inside emp_details
                                file_data["users"].append(a_dict)
                                # Sets file's current position at offset.
                                file.seek(0)
                                # convert back to json.
                                json.dump(file_data, file, indent = 4)
                                file.truncate()
                                
                            userArray = []

    def setCounter(self):
        self.wtfCounterLabel.configure(text=self.getCounter())
    
    def counter(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        with open(usersFile,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Add to global wtf counter
            for row in file_data['wtfCounter']:
                row["counter"] += 1

            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            file.truncate()

        # Add wtf to user
        self.counterUser(username, password)

        self.achivements()

        # Refresh the counter
        self.setCounter()
        
        # Log date and time
        self.logCounter()
        self.writeCsv()

        # Show Gif
        self.randomGif()

    # Menus and Shit

    def showUserMenu(self):
        self.wtfCounterLabel.place_forget()
        self.wtfTitleLabel.place_forget()
        # Show username and password fields
        self.usernameEntry.place(relx=0.369, rely=0.222, height=35
                , relwidth=0.264)
        self.usernameLabel.place(relx=0.43, rely=0.156, height=22, width=89)
        self.passwordEntry.place(relx=0.369, rely=0.444, height=35
                , relwidth=0.264)
        self.passwordLabel.place(relx=0.415, rely=0.378, height=22, width=109)
        self.closeBtn.place(relx=0.661, rely=0.089, height=28, width=47)

    def closeUserMenu(self):
        # Show Wtf label and counter
        self.wtfTitleLabel.place(relx=0.5, rely=0.22, height=45, width=435, anchor=CENTER)
        self.wtfCounterLabel.place(relx=0.5, rely=0.4, height=33, width=247, anchor=CENTER)
        
        # Rest entries
        self.usernameEntry.delete(0, END)
        self.passwordEntry.delete(0, END)

        # Hide user create stuff
        self.usernameEntry.place_forget()
        self.usernameLabel.place_forget()
        self.passwordEntry.place_forget()
        self.passwordLabel.place_forget()
        self.closeBtn.place_forget()

if __name__ == '__main__':
    try:
        vp_start_gui()
    except(KeyboardInterrupt, SystemExit):
        sys.exit()

sys.exit()
