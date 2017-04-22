from os import system
from time import sleep
import threading

JOKES = [('I asked my mom if by any chance I was adopted', 'She said, why would we choose you'), \
('Communism jokes are not funny', 'unless everyone gets them'), \
('I wish I could be ugly for one day', 'Because being ugly everyday sucks'), \
('This project'), \
('My boss pulled up in his new BMW today', 'He told me to work hard, put the hours in, and he will have an even better one next year'), \
('Funny that when a guy sleeps with tons of girls, hes a stud', 'But when I do this,somehow I am gay'), \
('My wife told me to get some pills for my erectile dysfunction', 'She went absolutely bonkers when I gave her some diet pills')]

NUM_JOKES = 8

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
    print("wrapper called, seed %s" % seed)
    speak("Here is a joke")
    sleep(1)
    print("post sleep")
    for i in JOKES[seed]:
        speak(i)
        sleep(0.5)
