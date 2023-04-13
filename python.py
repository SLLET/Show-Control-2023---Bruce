   #!/usr/bin/env python

import tkinter as tk
import datetime
import time
from pythonosc import udp_client
from pythonosc import osc_message_builder
from PIL import ImageTk, Image
from threading import Thread

def now():
    return datetime.datetime.now().astimezone()

scriptstart = now()
file="Logs/"+now().date().isoformat()+" "+now().time().isoformat()[0:8].replace(':','-')+".log"

def pw(*text):
    pout = str(now()) + " "
    with open(file,"a") as f:
        f.write(str(now())+" ")
        for t in text:
            t=str(t)
            f.write(t+" ")
            pout += t + " "
            f.write("\n")
    print(pout)

pw("Script Start")

def send_osc(message, address="192.168.2.10", port=53000):
    client = udp_client.SimpleUDPClient(address, port)
    msg = osc_message_builder.OscMessageBuilder(address = message)
    msg = msg.build()
    client.send(msg)
    return "OSC Message Sent"

def alivetime():
    global scriptstart
    delta = now() - scriptstart
    days = delta.days
    hours = int(delta.seconds / 3600)
    minutes = int(delta.seconds / 60) - (hours * 60)
    seconds = delta.seconds - (hours * 3600) - (minutes * 60)
    days = str(days)
    hours = "0" + str(hours)
    minutes = "0" + str(minutes)
    seconds = "0" + str(seconds)
    out = days+":"+hours[-2:]+":"+minutes[-2:]+":"+seconds[-2:]
    return "Uptime: "+out

def win():
    pw("Win")
    inputtxt.config(state="readonly")
    printButton.config(state="disabled")
    background.create_text(960,200, text=" Welcome BenSamZ ",fill="magenta",font=("Flood std", 90,  'bold'), anchor="center")
    #time.sleep(1)
    pw(send_osc('/cue/{8}/stop'))
    pw(send_osc('/cue/{10}/go'))

def tryagain():
    global tryagaintxt
    pw("No Win")
    tryagaintxt.grid(column = 0, row = 2)
    inputtxt.config(state="readonly")
    time.sleep(2)
    
    inputtxt.config(state="normal")
    inputtxt.delete(0,'end')
    tryagaintxt.destroy()
    tryagaintxt = tk.Label(password, text="Try Again",font=("Montserrat", 20, "italic"), justify="left", anchor="w")

def printInput(*none):
    inp = inputtxt.get()
    pw("Password Inputted:",inp)
    if inp == "test":
        Thread(target=win).start()
    else:
        Thread(target=tryagain).start()

my_w = tk.Tk()
width,height=1920,1080 # set the variables 
d=str(width)+"x"+str(height)
width,height=1920,1080 # set the variables

def runTask():
    global inputtxt
    global printButton
    global background
    global tryagaintxt
    global password
    my_w.geometry(d)
    my_w.configure(bg='#000000')
    my_w.title("Ben")

    background = tk.Canvas(my_w, width=1920, height=1080)

    bgimage = Image.open("ben.png")
    bgimage = bgimage.resize((1546,870), Image.LANCZOS)
    bgimage = ImageTk.PhotoImage(bgimage)

    background.create_image(960,540,anchor="center",image=bgimage)

    background.create_text(200,870, text=" Ben's Super Secret Login Page ",font=("Montserrat", 50,  'bold'),fill="blue", anchor="w")
    background.create_text(200,790, text=" SLLET ",fill="magenta",font=("Flood std", 90,  'bold'), anchor="w")
    background.place(relx=0.5,rely=0.5,anchor="center")

    password = tk.Frame(my_w, padx=5, pady=5)


    usertxt = tk.Label(password, text="Username: ",font=("Montserrat", 20), justify="left", anchor="w")
    usertxt.grid(column = 0, row = 0)

    bentxt = tk.Entry(password, width = 20, font=("Montserrat", 20))
    bentxt.insert(0, 'BenSamZ')
    bentxt.config(state="readonly")
    bentxt.grid(column = 1, row = 0)

    pwdtxt = tk.Label(password, text="Password: ",font=("Montserrat", 20), justify="left", anchor="w")
    pwdtxt.grid(column = 0, row = 1)

    # TextBox Creation
    inputtxt = tk.Entry(password, width = 20, font=("Montserrat", 20))
    inputtxt.grid(column = 1, row = 1)
    inputtxt.bind('<Return>', printInput)
    inputtxt.focus()
      
    # Button Creation
    printButton = tk.Button(password, text = "Enter", command = printInput, font=("Montserrat", 20,  'bold'))
    printButton.grid(column = 1, row = 2)

    password.place(relx=0.05,rely=0.3,anchor="w")

    tryagaintxt = tk.Label(password, text="Try Again",font=("Montserrat", 20, "italic"), justify="left", anchor="w")

    #password = tk.Text(my_w, height=1, width=30, font=("Montserrat", 20))
    #password.pack()
    #password.insert(tk.END, "Just a text Widget\nin two lines\n")

    my_w.attributes("-fullscreen", True)
    my_w.mainloop()

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    if address == "/start":
        runTask()
    
dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = ""
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Ready")
#runTask()
server.serve_forever()  # Blocks forever
print("End")
