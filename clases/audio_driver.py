import sounddevice # Al importar esta libreria desaparecen los mensajes de alertas de ALSA
import speech_recognition as sr
import subprocess
import locale
import re
from gtts import gTTS
from io import BytesIO
from os import system

from threading import Thread
from datetime import datetime
from pygame import mixer, time

from clases.utils import *

from config import COMANDOS_ACTIVACION, COMANDOS_ACCION

class AudioDriver():
    def __init__(self):
        """
        Inicializa la clase AudioDriver.

        Este método inicializa los siguientes atributos:
        - texto_global: Una variable para almacenar el texto del comando procesado.
        - codificacion: La codificación preferida de la configuración regional actual.
        - activacion: Una lista de comandos de activación.
        - Llama al método inicia_drivers_audio.
        - Imprime un mensaje indicando la inicialización de los controladores de audio.

        Parámetros:
        None

        Retorna:
        None
        """
        
        self.texto_global = None
        self.codificacion = locale.getpreferredencoding()

        if COMANDOS_ACTIVACION:
            self.activacion = COMANDOS_ACTIVACION
        else:
            raise ValueError(f'ERORR.: No hay comandos de activacion')

        self.stop_listening = False

        self.inicia_drivers_audio()
        

        print(f'{azul}Detectando Drivers de Sonido...\n{gris}')
        
    def activar(self, comando):
        """
        Busca y devuelve el comando de activación que se encuentra en el texto de entrada.

        Parámetros:
        comando (str): El texto de entrada donde se buscará el comando de activación.

        Retorna:
        str: El comando de activación encontrado en el texto de entrada, o 'False' si no se encuentra ninguno.
        """
        for act in self.activacion:
            if act.lower() in comando.lower():
                return act.lower()
        return False
    
    def texto_en_comando(self, texto, comando):
        """
        Busca y devuelve una coincidencia exacta de palabras en el texto de entrada.

        Utiliza expresiones regulares para buscar una coincidencia exacta de palabras en el texto de entrada,
        ignorando mayúsculas y minúsculas.

        Parámetros:
        texto (str): La palabra o frase que se buscará en el texto de entrada.
        comando (str): El texto de entrada donde se buscará la palabra o frase.

        Retorna:
        _sre.SRE_Match: Un objeto de coincidencia si se encuentra una coincidencia exacta de palabras, o 'None' si no se encuentra ninguna.
        """
        return re.search(r'\b' + texto + r'\b', comando, flags=re.IGNORECASE)


    def procesar_comando(self, comando):
        """
        Procesa el comando de entrada y ejecuta la acción correspondiente.

        Este método compara el comando de entrada con los comandos predefinidos (HORA, SALIR, FINALIZAR)
        y realiza la acción correspondiente. Si el comando no coincide con ninguno de los comandos predefinidos,
        devuelve el comando original.

        Parámetros:
        comando (str): El comando de entrada que se va a procesar.

        Retorna:
        str: El resultado del procesamiento del comando. Puede ser 'None', 'salir', 'finalizar' o el comando original.
        """
        if self.texto_en_comando(COMANDOS_ACCION[0], comando):
            ahora_local = datetime.now()
            print(f'\33[K{magenta}Son las.: {ahora_local.hour} con {ahora_local.minute} minutos{gris}')
            self.texto_a_audio(f'Son las.: {ahora_local.hour} con {ahora_local.minute} minutos')
            return None
        elif self.texto_en_comando(COMANDOS_ACCION[1], comando):
            self.texto_a_audio("Bien, limpiaré tu pantalla")
            system("clear")
            print(f'{rojo}Escuchando...      {gris}')
            return None
        
        elif self.texto_en_comando(COMANDOS_ACCION[2], comando):
            print(f'\33[K{magenta}Buscando en Google{gris}')
            self.texto_a_audio("Usted quiere buscar en google...")  
            parts = comando.split(COMANDOS_ACCION[2], 1)
            texto = parts[1].strip()
            return f"to_google {texto}"
            
        elif self.texto_en_comando(COMANDOS_ACCION[3], comando):
            print(f'\33[K{magenta}Usted dijo.: Quiero salir{gris}')
            self.texto_a_audio("Usted dijo que quiere salir, gracias...")
            return "salir"

        elif self.texto_en_comando(COMANDOS_ACCION[4], comando):
            print(f'\33[K{magenta}Usted dijo.: Finalizar{gris}')
            self.texto_a_audio("Entendido, tienes otra pregunta?")      
            return "finalizar"

        else:
            return comando

    def reconocer_voz(self, recognizer, audio):
        """
        Reconoce el audio proporcionado utilizando la API de Google Speech Recognition y procesa el comando.

        Este método utiliza la biblioteca 'speech_recognition' para transcribir el audio proporcionado en texto.
        Luego, verifica si el comando transcrito coincide con algún comando de activación. Si se encuentra una coincidencia,
        se procesa el comando utilizando el método 'procesar_comando' y se almacena el resultado en 'texto_global'.
        Si se produce alguna excepción durante el proceso de reconocimiento de voz, se limpia la variable 'transcripcion'.

        Parámetros:
        recognizer (speech_recognition.Recognizer): Un objeto Recognizer de la biblioteca 'speech_recognition'.
        audio (speech_recognition.AudioData): Un objeto AudioData que contiene el audio a transcribir.

        Retorna:
        None
        """
        if not self.stop_listening:
            try:
                print(f'{azul2}Reconociendo voz...{gris}')
                cursor_arriba()

                transcripcion = recognizer.recognize_google(audio, language = 'es-AR')

                activar = self.activar(transcripcion)
                if activar:
                    self.texto_global = self.procesar_comando(transcripcion)

                    transcripcion = None

                
                print(f'{rojo2}Reconociendo voz...{gris}')
                cursor_arriba()

            except Exception:
                transcripcion = None # Si no reconoce el audio limpia la variable transcripcion
                pass

    def texto_a_audio(self, texto):
        """
        Convierte un texto dado en audio y lo reproduce utilizando la biblioteca gTTS (Google Text-to-Speech).
        La función también ajusta la velocidad del audio utilizando ffmpeg.

        Parámetros:
        texto (str): El texto a convertir en audio.

        Retorna:
        None
        """
        if texto:

            tts = gTTS(texto, lang='es')

            with BytesIO() as f:
                tts.write_to_fp(f)
                f.seek(0)

                res = subprocess.run(
                    'ffmpeg -i pipe:0 -filter:a atempo=1.2 -f wav pipe:1',
                    shell = True,
                    input = f.read(),
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    check = True

                )
                audio_data = res.stdout
                audio_file = BytesIO(audio_data)
                mixer.music.load(audio_file)
                mixer.music.play()

                while mixer.music.get_busy():
                    time.delay(300)

    def thread_texto_a_audio(self, texto):     
        """
        Crea un hilo para convertir un texto dado en audio y reproducirlo.

        Utiliza la variable de instancia 'tts_thread' para almacenar la referencia al hilo.

        Parámetros:
        texto (str): El texto a convertir en audio.

        Retorna:
        None
        """
        self.tts_thread = Thread(target=self.texto_a_audio, args=(texto,))
        self.tts_thread.start()
    
    def devolver_contenido(self):
        """
        Devuelve el contenido almacenado en la variable 'texto_global' y lo borra.

        Si la variable 'texto_global' contiene algún texto, este método lo almacena en la variable 'contenido',
        borra el contenido de 'texto_global' y devuelve 'contenido'. Si 'texto_global' está vacío,
        este método devuelve 'None'.

        Parámetros:
        None

        Retorna:
        str: El contenido almacenado en 'texto_global' antes de borrarlo. Si 'texto_global' está vacío, devuelve 'None'.
        """
        if self.texto_global:
            contenido = self.texto_global
            self.texto_global = None
            return contenido
        else:
            return None
        
    def inicia_drivers_audio(self):
        """
        Inicializa los drivers de audio y configura el reconocimiento de voz.

        Utiliza la biblioteca 'pygame' para inicializar el mixer de audio y la biblioteca 'speech_recognition'
        para crear un objeto Recognizer y un objeto Microphone. Ajusta el ruido ambiente en el micrófono para
        mejorar la precisión del reconocimiento de voz. Finalmente, inicia el proceso de escucha en segundo plano
        para que el reconocimiento de voz se ejecute en segundo plano.

        Parámetros:
        None

        Retorna:
        None
        """
        mixer.init()

        self.api = sr.Recognizer()
        self.microphone = sr.Microphone()

        with self.microphone as fuente:
            self.api.adjust_for_ambient_noise(fuente)
        # Escucha en segundo plano
        self.api.listen_in_background(fuente, self.reconocer_voz)
    
    def __del__(self):
        # Cierra el proceso de escucha en segundo plano del reconocedor de voz
        self.stop_listening = True
        self.listen_thread.join()
       
