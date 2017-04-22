from os import system
from time import sleep

def speak(sentence):
    system('say -v Daniel "' + sentence + '"')


