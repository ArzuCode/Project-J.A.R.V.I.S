import sounddevice as sd
import wave
import numpy as np
import requests

# Səs yazmaq üçün parametrlər
SAMPLE_RATE = 44100  # Nümunə sürəti (Hz)
DURATION = 5  # Yazma müddəti (saniyə)
FILENAME = "output.wav"  # Yazılan səsin fayl adı

# Səs yazma funksiyası
def record_audio():
    print("Səs yazılır... Mikrofonunuza danışın.")
    recording = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=2, dtype='int16')
    sd.wait()  # Yazma tamamlanana qədər gözləyir
    print("Səs yazıldı.")
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())

# Səs oynatma funksiyası
def play_audio():
    print("Səs oynadılır...")
    with wave.open(FILENAME, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype='int16')  # Bytes formatını numpy array-ə çevirir
        sd.play(data, samplerate=SAMPLE_RATE)
        sd.wait()  # Oynatma tamamlanana qədər gözləyir

# Səs yazma parametrləri
SAMPLE_RATE = 44100  # Nümunə sürəti
DURATION = 5  # Yazma müddəti (saniyə)
FILENAME = "command.wav"  # Səs faylı adı

# Səs yazma funksiyası
def record_voice():
    print("Səs yazılır... Mikrofonunuza danışın.")
    recording = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=2, dtype='int16')
    sd.wait()  # Yazma tamamlanana qədər gözləyir
    print("Səs yazıldı.")
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())

# Google Speech-to-Text API istifadə edərək səs tanıma
def recognize_speech_google():
    api_url = "https://speech.googleapis.com/v1/speech:recognize?key=YOUR_API_KEY"  # Burada API açarınızı daxil edin
    headers = {
        "Content-Type": "application/json"
    }
    # Səsi Base64 formatına çevir
    with open(FILENAME, "rb") as audio_file:
        audio_content = audio_file.read()

    # Google API-ya göndərilən sorğu
    request_payload = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": SAMPLE_RATE,
            "languageCode": "az-AZ"  # Azərbaycan dili üçün
        },
        "audio": {
            "content": audio_content.decode('latin1')  # Base64 formatı
        }
    }

    try:
        print("Səs Google API-ya göndərilir...")
        response = requests.post(api_url, headers=headers, json=request_payload)
        response_data = response.json()

        if "results" in response_data:
            recognized_text = response_data["results"][0]["alternatives"][0]["transcript"]
            print(f"Tanınan mətn: {recognized_text}")
            return recognized_text
        else:
            print("Səs tanınmadı.")
            return None
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

def calculator():
      print("Kalkulyator aktivdir. Riyazi əməliyyatları yerinə yetirə bilərsiniz.")
      print("Əməliyyatlar: + (Toplama), - (Çıxma), * (Vurma), / (Bölmə)")
    
      while True:
        try:
            num1 = float(input("Birinci ədədi daxil edin: "))
            operator = input("Əməliyyatı daxil edin (+, -, *, /): ")
            num2 = float(input("İkinci ədədi daxil edin: "))
            
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 == 0:
                    print("Xəta: Bölmə sıfıra görə edilə bilməz!")
                    continue
                result = num1 / num2
            else:
                print("Yanlış operator daxil etdiniz!")
                continue
            
            print(f"Nəticə: {result}")
        except ValueError:
            print("Xəta: Yalnız sayılar daxil edin.")
        
        another_calculation = input("Başqa əməliyyat etmək istəyirsiniz? (bəli/xeyr): ").lower()
        if another_calculation != "bəli":
            break

# Əsas funksiya
def main():
    record_voice()
    command = recognize_speech_google()
    if command:
        print(f"Tanıdığım əmr: {command}")
    else:
        print("Heç bir əmr tanınmadı.")
    while True:
        print("\nJarvis: Mən hazıram. Nə etmək istədiyinizi deyin.")
        print("1. Səs yazmaq")
        print("2. Səs oynatmaq")
        print("3. Çıxış")
        choice = input("Seçim edin (1/2/3): ")

        if choice == '1':
            record_audio()
        elif choice == '2':
            play_audio()
        elif choice == '3':
            print("Jarvis dayandırılır...")
            break
        else:
            print("Yanlış seçim. Təkrar cəhd edin.")

if __name__ == "__main__":
    main()

from datetime import datetime

# Vaxt və tarixi qaytaran funksiya
def get_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Saat:dəqiqə:saniyə formatı
    current_date = now.strftime("%d-%m-%Y")  # Gün-ay-il formatı
    return f"Bu günün tarixi: {current_date}\nCari vaxt: {current_time}"


# OpenWeather API parametrləri
API_KEY = "???"  # Buraya öz açarınızı yazın
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Hava proqnozunu əldə edən funksiya
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

# Vaxt və tarixi qaytaran funksiya
def get_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Saat:dəqiqə:saniyə formatı
    current_date = now.strftime("%d-%m-%Y")  # Gün-ay-il formatı
    return f"Bu günün tarixi: {current_date}\nCari vaxt: {current_time}"

# Qlobal xatırlamalar siyahısı
reminders = []

# Xatırlatma əlavə etmək funksiyası
def add_reminder():
    reminder = input("Xatırlatma mətnini daxil edin: ")
    reminders.append(reminder)
    print("Xatırlatma əlavə olundu!")

# Mövcud xatırlamaları göstərmək funksiyası
def show_reminders():
    if reminders:
        print("Mövcud xatırlamalar:")
        for i, reminder in enumerate(reminders, start=1):
            print(f"{i}. {reminder}")
    else:
        print("Heç bir xatırlatma yoxdur.")

# Xatırlatma silmək funksiyası
def delete_reminder():
    if reminders:
        show_reminders()
        try:
            index = int(input("Silinməli olan xatırlamanın nömrəsini daxil edin: ")) - 1
            if 0 <= index < len(reminders):
                deleted = reminders.pop(index)
                print(f"Xatırlatma silindi: {deleted}")
            else:
                print("Yanlış nömrə daxil etdiniz.")
        except ValueError:
            print("Zəhmət olmasa, düzgün nömrə daxil edin.")
    else:
        print("Silinəcək xatırlatma yoxdur.")

from bs4 import BeautifulSoup

# Vebdən məlumat axtarma funksiyası
def search_web(query):
    print(f"Web-də '{query}' ilə əlaqəli məlumatlar axtarılır...")
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})
        print("\nAxtarış Nəticələri:")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result.get_text()}")
    else:
        print("Məlumatlar tapılmadı. Yenidən cəhd edin.")


# Əsas funksiya
def main():
    record_voice()
    command = recognize_speech_google()
    if command:
        print(f"Tanıdığım əmr: {command}")
    else:
        print("Heç bir əmr tanınmadı.")
    print("Jarvis başlatıldı...")
    
    while True:
        print("\nSeçimlər:")
        print("1. Hava proqnozunu öyrən")
        print("2. Vaxt və tarixi öyrən")
        print("3. Xatırlatma əlavə et")
        print("4. Mövcud xatırlamaları göstər")
        print("5. Xatırlatma sil")
        print("6. Vebdən məlumat axtar")
        print("7. Kalkulyator")
        print("8. Çıxış")
        
        choice = input("Seçiminizi daxil edin: ")
        
        if choice == "1":
            city = input("Hansı şəhər üçün hava məlumatı istəyirsiniz? ")
            weather_info = get_weather(city)
            print(weather_info)
        elif choice == "2":
            time_and_date = get_time_and_date()
            print(time_and_date)
        elif choice == "3":
            add_reminder()
        elif choice == "4":
            show_reminders()
        elif choice == "5":
            delete_reminder()
        elif choice == "6":
            query = input("Hansı mövzu ilə bağlı məlumat axtarırsınız? ")
            search_web(query)
        elif choice == "7":
            calculator()
        elif choice == "8":
            print("Jarvis bağlanır. Sağ olun!")
            break
        else:
            print("Yanlış seçim etdiniz. Yenidən cəhd edin!")

if __name__ == "__main__":
    main()
