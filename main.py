#importing tkinter library for GUI
from os import name
from tkinter import *
from tkinter import ttk
#importing subprocess so we can use system command
import subprocess
#import the re module so we can use regular expression
import re
#image python package
from PIL import ImageTk,Image




###########################################
###########################################
###########################################
########  FUNCTION SECTION ################
###########################################
###########################################
###########################################

def show():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)
    displayTable(wifi_list)


def displayTable(Wlist):
    i=0
    for el in Wlist:
        my_wifi_tree.insert(parent='',index='end',iid=i,text="",values=(el['ssid'],el['password']))
        i+=1

  

####################################################
#############   MAIN STRUCTURE  ####################
####################################################


root = Tk()
root.title("Wifi Password Windows 10")
root.geometry("400x600")
root.iconbitmap("wifi-logo.ico")
root.configure(bg="#0366ff")
root.resizable(0,0) #Don't Allow resizing in the x or y direction

wifi_img = Image.open("wifi-logo.png")
MAX_SIZE = (200,200)
wifi_img.thumbnail(MAX_SIZE)
logo_img = ImageTk.PhotoImage(wifi_img)
label_img = Label(image=logo_img,bg="#0366ff")
label_img.place(x=100,y=50)


#defining Table
my_wifi_tree = ttk.Treeview(root)
#columns 
my_wifi_tree['columns']=("WIFI","Password")
#define columns
my_wifi_tree.column("#0",width=0)
my_wifi_tree.column("WIFI",anchor=W,width=120,minwidth=30)
my_wifi_tree.column("Password",anchor=W,width=120,minwidth=30)
#define Headings
my_wifi_tree.heading("#0",text="",anchor=W)
my_wifi_tree.heading("WIFI",text="Wifi Name",anchor=W)
my_wifi_tree.heading("Password",text="Password",anchor=W)



my_wifi_tree.place(x=70,y=300)

                                                                


button_quit = Button(root,text="Start",command=show,width=30,fg="red",bg="yellow")
button_quit.place(x=80,y=550)



root.mainloop()

