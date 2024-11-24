import sounddevice as sd
import wave
import numpy as np

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

# Əsas funksiya
def main():
    record_audio()
    play_audio()

if __name__ == "__main__":
    main()
