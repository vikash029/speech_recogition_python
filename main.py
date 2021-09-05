import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import cv2
import imutils
from facial_emotion_recognition import EmotionRecognition


listener = sr.Recognizer()
engine = pyttsx3.init()
listener.energy_threshold = 300

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:


            print('listening...')

            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace('alexa', ' ')
                print(command)





    except:
        pass
    return command

def run_alexa():
    command = take_command()
    print(command)
    if "play" in command:
        song = command.replace('play','')
        talk('playing'+ song)
        pywhatkit.playonyt(song)
    elif "search" in command:
        se = command.replace("search"," ")
        talk("great" + se)
        pywhatkit.search(se)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('current time is ' + time)
    elif 'who is ' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 5)
        print(info)
        talk(info)
    elif "date" in command:
        talk("sorry, I have a boyfriend")
    elif "are you single" in command:
        talk("I am in a relationship in kuku")
    elif "joke" in command:
        talk(pyjokes.get_joke())
    elif "hello" in command:
        talk("hello who are you" " how may i help you ")
    elif "and you" in command:
        talk("am good" "how may i help you")

    elif "call" in command:
        pywhatkit.sendwhatmsg("datetime.datetime.now()")

    elif "search" in command:

        google = command.replace('search', '')
        print(google)
        talk('search' + google)
        pywhatkit.search(google)
    elif "open camera" in command:
       vs = cv2.VideoCapture(0)
       talk("camera open")
       while True:
             _,img = vs.read()
             cv2.imshow('videostream',img)
             key = cv2.waitKey(2) & 0xff

             if key == ord('q'):
               break
       cv2.waitKey(0)
       vs.release()
    elif "open image" in command:
        talk("image open")
        img = cv2.imread("G:\IMG.jpg")
        cv2.imshow("original", img)
        cv2.imwrite("IMG.jpg", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif "selfie" in command:
        talk("say chese")
        cam = cv2.VideoCapture(0)

        _, img = cam.read()
        cv2.imwrite("imagefromCamera.jpg", img)
        cv2.imshow("imagefromCamera.jpg", img)
        cam.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif "detected me" in command:
        cam = cv2.VideoCapture(0)

        firstFrame = None
        area = 500
        while True:
            _, img = cam.read()
            text = "Normal"
            img = imutils.resize(img, width=500)
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)
            if firstFrame is None:
                firstFrame = gaussianImg
                continue
            imgDiff = cv2.absdiff(firstFrame, gaussianImg)
            "threah img impROVEd pig"
            threahImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
            threahImg = cv2.dilate(threahImg, None, iterations=2)
            "cnta = help find never for thing "
            cnts = cv2.findContours(threahImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            count = 0

            for c in cnts:
                if cv2.contourArea(c) < area:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count = count + 1
                text = 'moving object detected' + str(count)
                print(text)
            cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.imshow("cameraFeed", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        cv2.waitKey(0)
        cam.release()

        cv2.destroyAllWindows()
    elif "face" in command:
        alg = 'G:\haarcascade_frontalface_default.xml'
        haar_cascade = cv2.CascadeClassifier(alg)
        cam = cv2.VideoCapture(0)

        while True:
            _, img = cam.read()
            text = 'no person detected'
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = haar_cascade.detectMultiScale(grayImg, 1.3, 4)

            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = 'person detected'
                (cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2))

            if text == text:
                (cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2))

            cv2.imshow('facedetection', img)
            key = cv2.waitKey(10)
            if key == 27:
                break
            if key == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
    elif "emotion" in command:



        er = EmotionRecognition(device='cpu')
        cam = cv2.VideoCapture(0)
        while True:
            sucess, frame = cam.read()
            frame = er.recognise_emotion(frame, return_type='BGR')
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cam.release()
        cv2.destroyAllWindows()










    else:
        talk(" sorry could not understand audio")

while True:
    run_alexa()
