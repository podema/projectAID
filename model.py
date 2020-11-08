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
import logging


class Model():
    def __init__(self):
        self.log = logging.getLogger('SpeechRecognition')
        self.cbs = []
    
    def addSpeechHandler(self, cb):
        self.cbs.append(cb)
    
    def removeSpeechHandler(self, cb):
        try:
            self.cbs.remove(cb)
        except ValueError:
            pass

    def callback(self, recognizer, audio):
        global stop
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            speech = recognizer.recognize_google(audio)
            self.log.debug("You are saying: " + speech)
            for cb in self.cbs:
                cb(speech)
            # if "bye" in speech:
            #     self.log.debug("Bye is in the speech!")
            #     self.stop()
        except sr.UnknownValueError:
            self.log.debug("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.log.debug("Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def start(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        stop = False
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)


    def stop(self):
        # calling this function requests that the background listener stop listening
        self.stop_listening(wait_for_stop=False)
