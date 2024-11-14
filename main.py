
from os import environ
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
    texto_terminal = TextoTerminal()
    audio_driver = AudioDriver()

    text = 'Buenas, para comunicarte conmigo debrás usar los siguientes comandos:'
    print(f'{verde}{text}\n{gris}')    
    audio_driver.thread_texto_a_audio(text)

    for comando in COMANDOS_ACTIVACION:
        print(f'{amarillo2}{comando}{gris}')

    sleep(5)
    text = 'Y para realizar algunas acciones debrá agregar las siguientes órdenes:'
    print(f'{verde}\n{text}\n{gris}')    
    audio_driver.thread_texto_a_audio(text)

    for comando in COMANDOS_ACCION:
        print(f'{amarillo2}{comando}{gris}')

    print(f'{rojo}\nEscuchando...{gris}')

    #sleep(1) 
    tmp_texto = None
    while True:
            voz = audio_driver.devolver_contenido()
            texto = texto_terminal.texto_ingresado
            if voz or texto:
                if len(texto.split()) > 20:
                    tmp_texto = ": " + texto
                    print(f'\33[K{azul2}\n{texto}\n{gris}')
                    audio_driver.texto_a_audio("El texto ingresado contiene más de 20 palabras. ¿Que desea hacer con él?")
                    texto = None

                comando = voz if voz else texto
                texto_terminal.texto_ingresado = ''
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

                print(f'{rojo}Escuchando...{gris}')
            # else:
            #     print(f'{rojo}Escuchando...{gris}')
            #     cursor_arriba()
            sleep(1)  # Reducir la carga del CPU
    exit()

if __name__ == '__main__':
    main()