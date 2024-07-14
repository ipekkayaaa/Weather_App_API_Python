from tkinter import *
from tkinter import Tk, PhotoImage, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import requests
import pytz
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)
root.configure(bg="#68838B")

# Define all tkinter widgets
textfield = None
clock = None
t = None
w = None
h = None
d = None
p = None
name = None


def getWeather():
    global textfield, clock, t, w, h, d, p, name

    city = textfield.get()

    try:
        geolocator = Nominatim(user_agent="geopExercises")
        location = geolocator.geocode(city)

        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(
                lng=location.longitude, lat=location.latitude)
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time, bg="#68838B")
            name.config(text="CURRENT WEATHER", bg="#68838B")

            # Fetch weather data
            api_key = os.getenv('MY_API_KEY')
            print(f"API Key: {api_key}")
            api = f"https://api.openweathermap.org/data/2.5/weather?q={
                city}&appid={api_key}"

            json_data = requests.get(api).json()

            # Update labels with weather data
            if 'weather' in json_data and len(json_data['weather']) > 0:
                condition = json_data['weather'][0]["main"]
                description = json_data['weather'][0]['description']
            else:
                condition = "N/A"
                description = "N/A"

            if 'main' in json_data:
                temp = int(json_data['main']['temp'] - 273.15)
                pressure = json_data['main']['pressure']
                humidity = json_data['main']['humidity']
            else:
                temp = 0
                pressure = 0
                humidity = 0

            if 'wind' in json_data:
                wind_speed = json_data['wind']['speed']
            else:
                wind_speed = 0

            # Update labels with weather data
            t.config(text=f"{temp}°")
            w.config(text=f"{wind_speed} m/s")
            h.config(text=f"{humidity}%")
            d.config(text=f"{description}")
            p.config(text=f"{pressure} hPa")

        else:
            messagebox.showerror("Error", f"Could not find location: {city}")

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")


# Load the images (assuming these are in the correct directory)
Search_image = PhotoImage(file="images/search.png")
Search_icon = PhotoImage(file="images/search_icon.png")
Logo_image = PhotoImage(file="images/logo.png")

# Create widgets with appropriate configurations
myimage = Label(root, image=Search_image, bg="#68838B")
myimage.place(x=20, y=20)

textfield = Entry(root, justify="center", width=17, font=(
    "poppins", 25, "bold"), bg="#262626", fg="white")
textfield.place(x=50, y=40)
textfield.focus()

myimage_icon = Button(root, image=Search_icon, borderwidth=0,
                      cursor="hand2",  bg="#68838B", command=getWeather)
myimage_icon.place(x=400, y=34)

logo = Label(root, image=Logo_image, bg="#68838B")
logo.place(x=150, y=100)

# Create a Frame for the bottom bar
frame_bottom = Frame(root, bg="white", width=800,
                     height=80, bd=1, relief=SOLID)
frame_bottom.place(x=50, y=400)

# Labels for weather details
Label(root, text="WIND", font=("Helvetica", 15, 'bold'),
      fg="#8A360F", bg="white").place(x=130, y=405)
Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'),
      fg="#8A360F", bg="white").place(x=265, y=405)
Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'),
      fg="#8A360F", bg="white").place(x=445, y=405)
Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'),
      fg="#8A360F", bg="white").place(x=665, y=405)

# Placeholder labels for weather data
t = Label(root, font=("arial", 70, "bold"),
          fg="#8B3A62", text="...", bg="#68838B")
t.place(x=400, y=150)

w = Label(root, text="...", font=(
    "arial", 20, "bold"), bg="white", fg="#8A360F")
w.place(x=130, y=440)

h = Label(root, text="...", font=(
    "arial", 20, "bold"), bg="white", fg="#8A360F")
h.place(x=275, y=440)

d = Label(root, text="...", font=(
    "arial", 20, "bold"), bg="white", fg="#8A360F")
d.place(x=460, y=440)

p = Label(root, text="...", font=(
    "arial", 20, "bold"), bg="white", fg="#8A360F")
p.place(x=665, y=440)

# Time labels
name = Label(root, font=("arial", 15, "bold"), text="...", bg="#68838B")
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20), text="...", bg="#68838B")
clock.place(x=30, y=130)

root.mainloop()
