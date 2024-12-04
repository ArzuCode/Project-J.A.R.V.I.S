# Import edilən kitabxanalar
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import requests
import json
from datetime import datetime

# Səsli cavab üçün tənzimləmə
engine = pyttsx3.init()

# GUI tərtibatı
class JarvisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jarvis")
        self.master.geometry("600x400")

        self.text_box = tk.Text(self.master, height=15, width=70)
        self.text_box.pack(pady=10)

        self.input_field = tk.Entry(self.master, width=50)
        self.input_field.pack(pady=5)

        self.send_button = tk.Button(self.master, text="Göndər", command=self.handle_command)
        self.send_button.pack()

    def handle_command(self):
        command = self.input_field.get().lower()
        self.text_box.insert(tk.END, f"Siz: {command}\n")
        self.input_field.delete(0, tk.END)

        if "hava" in command:
            city = "Baku"  # Standart olaraq Bakı
            weather = self.get_weather(city)
            self.text_box.insert(tk.END, f"Jarvis: {weather}\n")
            self.speak(weather)
        elif "vaxt" in command or "tarix" in command:
            time_date = self.get_time_and_date()
            self.text_box.insert(tk.END, f"Jarvis: {time_date}\n")
            self.speak(time_date)
        else:
            response = "Bağışlayın, bu əmri başa düşmədim."
            self.text_box.insert(tk.END, f"Jarvis: {response}\n")
            self.speak(response)

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def get_weather(self, city):
        try:
            api_key = "5e2ed3f7725133ea5249a99a113c3667"  # OpenWeather API açarı
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                description = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return f"{city} üçün hava: {description}, Temperatur: {temp}°C"
            else:
                return "Şəhər tapılmadı."
        except Exception as e:
            return f"Xəta: {e}"

    def get_time_and_date(self):
        now = datetime.now()
        return f"Tarix: {now.strftime('%Y-%m-%d')}, Vaxt: {now.strftime('%H:%M:%S')}"

# Proqramın işlədilməsi
if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisApp(root)
    root.mainloop()
