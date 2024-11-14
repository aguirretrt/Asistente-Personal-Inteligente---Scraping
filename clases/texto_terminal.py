
from threading import Thread

class TextoTerminal():
    texto_ingresado = ""

    def __init__(self):
        """
        Este constructor inicia un hilo demonio que lee continuamente la entrada del usuario. La entrada se almacena en el atributo 'texto_ingresado'.

        Atributos:
        texto_ingresado (str): Almacena la entrada del usuario.

        Métodos:
        input_thread: Lee la entrada del usuario y la almacena en 'texto_ingresado'.
        """
        self.texto_ingresado = ""
        self.hilo_texto = Thread(target=self.input_thread)
        self.hilo_texto.daemon = True
        self.hilo_texto.start()
        
    def input_thread(self):        
        while True:
            self.texto_ingresado = input()

    def __del__(self):        
        self.hilo_texto.join()
