import pyttsx3
import speech_recognition as sr
import pyaudio
import os
import random
import pywhatkit
response = pyttsx3.init()
listening = sr.Recognizer()
voices = response.getProperty("voices")
response.setProperty("voice", voices[1].id)
#fartList = [""" r'C:\\Users\\Sebastian\\alexaSounds\\fart1' """]
def opening():
    os.startfile(r'{FilePath}\powerOn.mp3')
    response.say("I am now listening")
    response.runAndWait()
def great():
    counter = 0
    chiri = True
    #response.say("command 'terminate' to quit")
    #response.runAndWait()
    while chiri:
        response = pyttsx3.init()
        listening = sr.Recognizer()
        try:
            with sr.Microphone() as mic: #changes sr.mic into source
                print("listening...")
                voice = listening.listen(mic) #.listen is built in command with sr? source refers to listen while using mic
                command = listening.recognize_google(voice)
                command = command.lower()
                print(command)
                #response.say(command)
                #response.runAndWait()
                if "hey prudence" in command:
                    print("How can I help you")
                    response.say("How can I help you")
                    response.runAndWait()
                elif "hey alexa" in command:
                    print("thats not me")
                    response.say("that's not me")
                    response.runAndWait()
                elif "terminate" in command:
                    response.say("Im going to bed")
                    response.runAndWait()
                    os.startfile(r'{FilePath}\powerOff.mp3')
                    spy = True
                    chiri = False
                elif "thank you" in command:
                    response.say("Your welcome fatty")
                    response.runAndWait()
                    
                elif "fart" in command:
                    os.chdir(r'{FilePath}\alexaSounds')
                    print(os.getcwd())
                    #os.startfile(r'C:\Users\Sebastian\Youtube\2seb sounds\Ape Escape - Beef.mp3')
                    num1 = random.randint(1,4)
                    print(num1)
                    if num1 == 1:
                        os.startfile(r'{FilePath}\fart7.mp3')
                    if num1 == 2:
                        os.startfile(r'{FilePath}\fart2.mp3')
                    if num1 == 3:
                        os.startfile(r'{FilePath}\fart3.mp3')
                    if num1 == 4:
                        os.startfile(r'{FilePath}\fart4.mp3')
                elif "play" in command:
                    if "by" in command:
                        #artist = string["by":]
                        removal = command.find("by")
                        artist = command[removal:]
                        finalArtist = artist.replace("by", "")
                        print(finalArtist)
                        song1 = command.replace("play", "")
                        song2 = song1.replace(artist, "")
                        print(song2)
                        pywhatkit.playonyt(song2 + finalArtist)
                        response.say("playing " + song2 + "by the artist" + finalArtist)
                        response.runAndWait()
                    else:
                        song = command.replace("play", "")
                        response.say("playing" + song)
                        response.runAndWait()
                        print(song)
                        pywhatkit.playonyt(song)
                elif "why" in command:
                    if "stupid" in command:
                        response.say("I'm not stupid you are")
                        response.runAndWait()
                    else:
                        response.say("Please repeat your question")
                        response.runAndWait()
        except:
            print("Sorry I didnt get that, try again")
            #response.say("Sorry, I didnt get that")
            #response.runAndWait()
            counter = counter + 1
            pass
        if counter == 5:
            print("your incoherent dude")
            counter = 0
            response.say("Im going to bed")
            response.runAndWait()
            os.startfile(r'{FilePath}\powerOff.mp3')
            chiri = False
opening()
spy = True
while spy:
    try:
        with sr.Microphone() as mic: #changes sr.mic into source
            print("listening...")
            voice = listening.listen(mic) #.listen is built in command with sr? source refers to listen while using mic
            command = listening.recognize_google(voice)
            command = command.lower()
            print(command)
            #response.say(command)
            #response.runAndWait()
            if "hey prudence" in command:
                print("How can I help you")
                response.say("How can I help you")
                response.runAndWait()
                chiri = True
                great()
    except:
        pass



