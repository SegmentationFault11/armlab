from os import system
from time import sleep
import threading

def speak(sentence):
    system('say -v Daniel "' + sentence + '"')

def tell_joke(seed):
    print("non wrapper called")
    joke_thread = threading.Thread(target = tell_joke_wrapper, args = (seed, ))
    joke_thread.daemon = True
    joke_thread.start()
    joke_thread.join()
    print("non wrapper finished")

def tell_joke_wrapper(seed):
    print("wrapper called")
    speak("Here is a joke")
    sleep(1)
    print("post sleep")
    if seed == 0:
        speak("I asked my mom if by any chance I was adopted")
        sleep(0.5)
        speak("She said, why would we choose you")
    elif seed == 1:
        speak("Communism jokes are not funny")
        sleep(0.5)
        speak("unless everyone gets them")
    elif seed == 2:
        speak("I wish I could be ugly for one day")
        sleep(0.5)
        speak("Because being ugly everyday sucks")
    elif seed == 3:
        speak("This project")
    elif seed == 4:
        speak("My boss pulled up in his new BMW today")
        sleep(0.5)
        speak("He told me to work hard, put the hours in, and he will have an even better one next year")
    elif seed == 4000:
        speak("Funny that when a guy sleeps with tons of girls, hes a stud")
        sleep(0.5)
        speak("But when I do this,somehow I am gay")
    elif seed == 4001:
        speak("My wife told me to get some pills for my erectile dysfunction")
        sleep(0.5)
        speak("She went absolutely bonkers when I gave her some diet pills")
    elif seed == 4002:
        speak("This project")

tell_joke(2)
