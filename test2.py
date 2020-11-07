#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

# TEST 2:
#   The client can talk during xx amount of time (for example, 20 seconds).
#   The program saves the audio content in a WAV file.
#   After that, the program analyze the WAV file and detects if the client needs help (detecting in the WAV file the word "HELP")

# Observations: This program (test2.py) detects better the words because analyze all the entire file. 

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as mic_source:
    r.adjust_for_ambient_noise(mic_source)  # we only need to calibrate once, before we start listening
    print("Say something!")
    audio = r.record(mic_source, 20)
    print("I've finished recording.")

# write audio in bainary mode ("wb") to a WAV file
with open("test2.wav", "wb") as f:
    f.write(audio.get_wav_data())

with sr.AudioFile("test2.wav") as file_content:
    print("Analyzing data...")
    audio = r.record(file_content)  # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    speech = r.recognize_google(audio)
    print("You said: " + speech)
    if "help" in speech:
        print("It seems that you need help!! Do you want to contact with the teacher?")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))



# # recognize speech using Sphinx
# try:
#     print("You said: " + r.recognize_sphinx(audio_en))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))