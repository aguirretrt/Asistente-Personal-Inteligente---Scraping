
from os import environ, path, listdir
from shutil import rmtree
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from sys import exit
from time import sleep

from clases.asistente import *
from clases.audio_driver import *
from clases.texto_terminal import *

from config import COMANDOS_ACTIVACION, COMANDOS_ACCION
def main():
    """
    Esta función inicializa los objetos y controladores necesarios, y luego entra en un bucle 
    donde escucha la entrada del usuario (voz o texto) y responde en consecuencia.
    La función también maneja comandos específicos e interacciones con las clases Asistente,
    TextoTerminal y AudioDriver.

    Parámetros:
    Ninguno

    Retorna:
    Ninguno
    """
    asistente = Asistente()
    asistente.ultima_conversacion()
    
    audio_driver = AudioDriver()
    texto_terminal = TextoTerminal()
    text = 'Buenas, para comunicarte conmigo debrás usar los siguientes comandos:'
    print(f'{verde}{text}\n{gris}')    
 
    for comando in COMANDOS_ACTIVACION:
        text = text + ", " + comando
        print(f'{amarillo2}{comando}{gris}')

    text2 = 'Y para realizar algunas acciones, debrá agregar las siguientes órdenes:'
    print(f'{verde}\n{text2}\n{gris}')    
    
    for comando in COMANDOS_ACCION:
        text2 = text2 + ", " + comando
        print(f'{amarillo2}{comando}{gris}')

    audio_driver.thread_texto_a_audio(text + ", " + text2)
    print(f'{rojo}\nEscuchando...      {gris}')

    tmp_texto = None
   
    while True:
            voz = audio_driver.devolver_contenido()
            texto = texto_terminal.obtener_texto()
            if voz or texto:
                if len(texto.split()) > 20:
                    tmp_texto = ": " + texto
                    print(f'\33[K{azul2}\n{texto}\n{gris}')
                    audio_driver.texto_a_audio("El texto ingresado contiene más de 20 palabras. ¿Que desea hacer con él?")
                    texto = None

                comando = voz if voz else texto
                #texto_terminal.texto_ingresado = ''
                if tmp_texto and comando is not None:
                    comando = comando + tmp_texto
                    tmp_texto = None
                acciones = {
                    'salir': lambda: None,
                    'finalizar': lambda: None,
                    'to_google': asistente.buscar_texto_en_navegador
                }
                if comando in acciones:
                    if comando == 'salir':                        
                        break  # Esta línea para romper el bucle
                elif comando:
                    if comando.startswith('to_google'):
                        asistente.buscar_texto_en_navegador(comando)
                    else:

                        print(f'\33[K{amarillo}{comando}{gris}')
                        respuesta = asistente.chatear(comando)
                        print(f'{verde}{respuesta}{gris}')
                        print()
                        # Envia la respuesta de texto a reproducir en audio
                        audio_driver.thread_texto_a_audio(respuesta)

                print(f'{rojo}Escuchando...      {gris}')

            sleep(1)  # Reducir la carga del CPU

    # Metodo para eliminar carpetas temporales creadas por la aplicacion
    for carpeta in listdir('/tmp'):
        ruta_completa = path.join('/tmp', carpeta)
        if path.isdir(ruta_completa) and (carpeta.startswith('.com.google') or carpeta.startswith('.org.chromium.')):
            try:
                rmtree(ruta_completa)
            except:
                pass

    exit()

if __name__ == '__main__':
    
    main()