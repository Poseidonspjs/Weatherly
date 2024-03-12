#imports
import customtkinter as cTk
import tkinter
import requests
from PIL import Image
from datetime import date
from time import sleep


#VARIABLES

#api
URL_BASE = "http://api.weatherbit.io/v2.0/current?"

file = open("api.txt", "r")
read = file.read()
API_KEY = read 


URL_IMG = "https://cdn.weatherbit.io/static/img/icons/"

#styling for widgets
widgetFG = "#292929"

#date stuff
today = date.today()
dT = today.strftime("%b, %d, %Y")



#functions

#submission function
def SUBMIT():

    city = city_entry.get()
    url = URL_BASE + "key=" + API_KEY + "&city=" + city #builds api req
    response = requests.get(url).json() #sends api req

    #data extracted from json
    ex = response['data'][0]
    cty = ex['city_name']
    app_temp = round(float(ex['app_temp'] * (9/5) + 32), 2)
    description = ex['weather']['description']

    #getting weather icon
    img = ex['weather']['icon']
    img_url = f"{URL_IMG}{img}.png"
    data_img = requests.get(img_url).content
    IMAGEJPG = open("img.jpg", "wb") #new img file
    IMAGEJPG.write(data_img)
    IMAGEJPG.close()

    #makes the data widget(s)
    def create():
        #test
        print("create test")

        #icon
        icon = cTk.CTkImage(dark_image=Image.open("img.jpg"),
                            size=(500, 500))
        
        #title
        CI = cTk.CTkLabel(master=info_frame, 
                            text=cty,
                            font=("Consolas", 90),
                            padx = 20, pady = 16,
                            fg_color=widgetFG,
                            corner_radius=8
                            )
        
        #temp (may add swapping functionality later (C to F or F to C))
        temp = cTk.CTkLabel(master = info_frame, 
                            text=f"{app_temp} F",
                            font=("Consolas", 50),
                            padx = 20, pady = 16)
        
        #Other info
        weather = cTk.CTkLabel(master=info_frame,
                               text= f"{description} \n {dT} ",
                               font=("Consolas", 30),
                               padx = 20, pady = 16
                               )
        
        #Icon
        w_icon = cTk.CTkLabel(master=icon_frame,
                              text="",
                              image=icon)
        
        #placing widgets
        CI.pack()
        temp.pack()
        weather.pack()
        w_icon.pack()
        app.update()
        
        
    #deletes old info widgets
    def deleteOldWidgets():
        for l in info_frame.pack_slaves():
            l.pack_forget()
        for l in icon_frame.pack_slaves():
            l.pack_forget()

    #run delete
    deleteOldWidgets()

    #run create
    create()
    
    #console info
    print()
    print(ex['city_name'])
    print(app_temp)
    print(dT)
    print(description)

    #delete enty
    city_entry.delete(0, 'end')
    city_entry.configure(state="disabled")
    sleep(2) #adds cooldown, so dont run out of too maany requests
    city_entry.configure(state="normal")

#slider command to change themes, currently is sorta working, actual widget colors are not changing
""""
def themeChange():
    if (theme_switch.get()==0):
        app._set_appearance_mode("dark")
    elif (theme_switch.get()==1):
        app._set_appearance_mode("light")
    

    global widgetFG 
    widgetFG = "white"
    app.update()
"""

#app init and configs
app = cTk.CTk()
app.geometry("1200x1000")
app._set_appearance_mode("dark")
app.title("Weatherly")

#switch vars
x = tkinter.IntVar()

#frame for logo/sidebar
logo_frame = cTk.CTkFrame(master=app, corner_radius=15, fg_color="transparent") #logo frame width=227, height=80
logo_frame.pack(anchor = "nw", fill="y")
#f1.pack()

#logo
logo = cTk.CTkLabel(master=logo_frame, text="Weatherly", anchor= "nw", font=("Consolas", 40), padx = 20, pady = 16, corner_radius=10, fg_color=widgetFG)    
logo.pack()
#l1.pack(padx=10, pady = 10)

#light or dark mode setting
#theme_frame = cTk.CTkFrame()
#theme_switch = cTk.CTkSwitch(master=app, text="theme", command=themeChange, variable= x, onvalue=1, offvalue=0)
#theme_switch.pack(side= "bottom", anchor="sw")

#submission frame
entry_frame = cTk.CTkFrame(master=app, width=500, height=100) #for some reason place() is just not working anymore?? @debug
#f2.place(relx=0, rely =1)
entry_frame.pack(side= "bottom")

#submission widgets for entering city/location
city_entry = cTk.CTkEntry(master=entry_frame, placeholder_text= "Enter City: ", width= 800, height= 32, font=("Consolas", 25))
city_entry.pack(side = "left", padx=5, pady= 10) #workaround for now, entry widget for city

submission = cTk.CTkButton(master=entry_frame, text="Submit", width=80, height=32, font=("Consolas", 20), command=SUBMIT)
submission.pack(side="right", padx=5, pady=10)

#frames for information, placed here in order for the delete function to work
info_frame = cTk.CTkFrame(master=app, fg_color="transparent")
info_frame.pack(fill="y")
icon_frame = cTk.CTkFrame(master=app, fg_color="transparent")
icon_frame.pack(fill="y")


app.mainloop()