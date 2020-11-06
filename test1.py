#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

# TEST 1: 
#   While the client is talking, the AI try to identify the words and show them on the screen.
#   If the AI detects the word "HELP", immediatly appears an alert on the screen.
#   The microphone is always on until detects the word "BYE", that is, the client want to leave.

# Observations: This program (test1.py) doesn't detect perfectly all the words because analyze sentence per sentence
# and sometimes doesn't detect the sentence correctly.

# Advantages: "Real-Time" detection and you don't have to create an external file.

import time

import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    global stop
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        speech = recognizer.recognize_google(audio)
        print("You are saying: " + speech)
        if "bye" in speech:
            #print("Bye is in the speech!")
            stop = True
        elif "help" in speech:
            print("It seems that you need help!! Do you want to contact with the teacher?")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
stop = False
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    print("Say something!")

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# wait until "Bye" is detected
while stop == False:
    time.sleep(0.1)

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)

# do some more unrelated things
for _ in range(50): time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping