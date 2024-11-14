
from os import environ
from subprocess import Popen, DEVNULL

class GoogleDriver():     
    @staticmethod
    def buscar(text = None):
        environ['DISPLAY'] = ':1'
        Popen(['google-chrome', 'https://www.google.com/search?q=' + text], stderr=DEVNULL)
