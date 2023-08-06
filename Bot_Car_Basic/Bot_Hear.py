import speech_recognition
from CA_Speak import play

def hear_first():
    ear = speech_recognition.Recognizer()
    while True:
        with speech_recognition.Microphone() as mic:
            ear.adjust_for_ambient_noise(mic, duration=5)
            print("-> ")
            audio = ear.listen(mic)
            try:
                # Chuyển đổi giọng nói thành văn bản
                text = ear.recognize_google(audio, language="vi")
                print(" ... ")
                text = text.lower()
            except:
                text = ""
            print("Yourself: {}".format(text))
            return text
def hear(x):
    ear = speech_recognition.Recognizer()
    while True:
        with speech_recognition.Microphone() as mic:
            ear.adjust_for_ambient_noise(mic, duration=5)
            play(x)
            audio = ear.listen(mic)
            try:
                # Chuyển đổi giọng nói thành văn bản
                text = ear.recognize_google(audio, language="vi")
                print(" ... ")
                text = text.lower()
            except:
                text = ""
            print("Yourself: {}".format(text))
            return text

def get_text():
    for i in range(3):
        text = hear("Bạn muốn xem thời tiết ở đâu")
        if text:
            return text.lower()
        elif i<3:
            play("Em vẫn chưa nghe rõ, Cậu nói lại được không")
            #time.sleep(2)
        else:
            play("Hẹn gặp cậu sau")
            return 0

