import queue
from sys import stdin
from threading import Thread 

class TextoTerminal():
    def __init__(self):
        self.texto_ingresado = queue.Queue()  # Cola para almacenar el texto ingresado
        self.hilo_texto = Thread(target=self.capturar_texto, daemon=True)
        self.hilo_texto.start()

    def capturar_texto(self):
        """Este hilo captura la entrada de texto del terminal y la almacena en la cola"""

        for linea in stdin:
            self.texto_ingresado.put(linea.strip())

    def obtener_texto(self):
        """Devuelve el texto capturado si está disponible"""
        if not self.texto_ingresado.empty():
            return self.texto_ingresado.get()
        return ""
    
    def __del__(self):
        """
        Finaliza el hilo adecuadamente.
        """
        if self.hilo_texto.is_alive():
            self.hilo_texto.join()