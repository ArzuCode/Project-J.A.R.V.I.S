import pyttsx3
import speech_recognition as sr
import json
import requests
from datetime import datetime
import wave
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import os

# Vosk modelini yükləyin (sadəcə ingilis dilində dəstəkləyir)
MODEL_PATH = "vosk-model-small-en-us-0.15"  # Modelin qovluq adı
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Səsli cavab üçün engine
engine = pyttsx3.init()

# Dil parametrləri
languages = {
    "en": "english",
    "az": "azerbaijani"
}
current_language = "az"  # Başlanğıcda Azərbaycan dili

# Qlobal dəyişənlər
reminders = []  # Xatırlama siyahısı
API_KEY = "5e2ed3f7725133ea5249a99a113c3667"  # OpenWeather API açarı
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
SAMPLE_RATE = 44100  # Nümunə sürəti (Hz)
DURATION = 5  # Yazma müddəti (saniyə)
FILENAME = "output.wav"  # Yazılan səs faylının adı

# ==== Səsli Cavab Vermə Funksiyası ====
def speak(text):
    engine.setProperty('rate', 150)  # Səsin sürəti
    engine.setProperty('volume', 1)  # Həcmi 1 (maksimum)
    
    if current_language == "az":
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Ahmet')  # Azərbaycan dili
    else:
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')  # İngilis dili
        
    engine.say(text)
    engine.runAndWait()

# ==== Səsli Komanda Tanıma Funksiyası ====
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinləyirəm... Danışın.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Tanıyıram...")
        if current_language == "az":
            command = recognizer.recognize_google(audio, language="az-AZ")
        else:
            command = recognizer.recognize_google(audio, language="en-US")
        
        print(f"Səsli Komanda: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Səs tanınmadı. Yenidən cəhd edin.")
        return ""
    except sr.RequestError as e:
        print(f"Xəta baş verdi: {e}")
        return ""

# ==== Vaxt və Tarixi Göstər ==== 
def get_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%Y")
    return f"Bu günün tarixi: {current_date}\nCari vaxt: {current_time}"

# ==== Hava Proqnozu ==== 
def get_weather(city):
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric&lang=az"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            return (f"{city} şəhəri üçün hava məlumatı:\n"
                    f"Vəziyyət: {weather.capitalize()}\n"
                    f"Temperatur: {temp}°C\n"
                    f"Hiss olunan: {feels_like}°C\n"
                    f"Rütubət: {humidity}%")
        else:
            return "Şəhər tapılmadı. Zəhmət olmasa, düzgün şəhər adı daxil edin."
    except Exception as e:
        return f"Xəta baş verdi: {e}"

# ==== Kalkulyator ==== 
def calculator():
    print("Kalkulyator aktivdir. Riyazi əməliyyatları yerinə yetirə bilərsiniz.")
    while True:
        try:
            num1 = float(input("Birinci ədədi daxil edin: "))
            operator = input("Əməliyyatı daxil edin (+, -, *, /): ")
            num2 = float(input("İkinci ədədi daxil edin: "))

            if operator == "+":
                print(f"Nəticə: {num1 + num2}")
            elif operator == "-":
                print(f"Nəticə: {num1 - num2}")
            elif operator == "*":
                print(f"Nəticə: {num1 * num2}")
            elif operator == "/" and num2 != 0:
                print(f"Nəticə: {num1 / num2}")
            else:
                print("Səhv operator və ya sıfıra bölmə.")
        except ValueError:
            print("Yalnız rəqəm daxil edin.")

        if input("Davam etmək istəyirsiniz? (bəli/xeyr): ").lower() != "bəli":
            break

# ==== Xatırlatma Funksiyaları ====
def add_reminder():
    reminder = input("Xatırlatma mətnini daxil edin: ")
    reminders.append(reminder)
    print("Xatırlatma əlavə olundu!")

def show_reminders():
    if reminders:
        for i, reminder in enumerate(reminders, start=1):
            print(f"{i}. {reminder}")
    else:
        print("Xatırlama yoxdur.")

def delete_reminder():
    if reminders:
        show_reminders()
        try:
            index = int(input("Silinməli olan xatırlamanın nömrəsini daxil edin: ")) - 1
            if 0 <= index < len(reminders):
                print(f"Silindi: {reminders.pop(index)}")
        except ValueError:
            print("Düzgün nömrə daxil edin.")
    else:
        print("Xatırlama yoxdur.")

# ==== Dil Seçimi ====
def change_language():
    global current_language
    print("Dil seçimi: \n1. Azərbaycan dili \n2. İngilis dili")
    choice = input("Seçiminizi daxil edin: ")

    if choice == "1":
        current_language = "az"
        speak("Azərbaycan dilinə keçid edildi.")
    elif choice == "2":
        current_language = "en"
        speak("Switched to English language.")
    else:
        speak("Yanlış seçim. Dil dəyişməyib.")

# ==== Əsas Funksiya ====
def main():
    print("Jarvis başlatıldı...")
    speak("Salam! Jarvis ilə ünsiyyətə başlaya bilərsiniz.")

    while True:
        print("\nSeçimlər:")
        print("1. Dil dəyişdir")
        print("2. Hava proqnozunu öyrən")
        print("3. Vaxt və tarixi öyrən")
        print("4. Xatırlatma əlavə et")
        print("5. Xatırlamaları göstər")
        print("6. Xatırlatma sil")
        print("7. Kalkulyator")
        print("8. Səs yaz")
        print("9. Səs oynat")
        print("10. Çıxış")

        # Komanda alırıq
        command = listen_for_command()

        if "dil" in command:
            change_language()
        elif "hava" in command:
            city = input("Şəhər adı: ")
            speak(get_weather(city))
        elif "vaxt" in command or "tarix" in command:
            speak(get_time_and_date())
        elif "xatırlatma" in command:
            if "əlavə et" in command:
                add_reminder()
            elif "göstər" in command:
                show_reminders()
            elif "sil" in command:
                delete_reminder()
        elif "kalkulyator" in command:
            calculator()
        elif "səs yaz" in command:
            record_audio()
        elif "səs oynat" in command:
            play_audio()
        elif "çıxış" in command:
            speak("Jarvis bağlanır. Sağ olun!")
            print("Jarvis bağlanır. Sağ olun!")
            break
        else:
            speak("Yanlış seçim. Yenidən cəhd edin!")

if __name__ == "__main__":
    main()
