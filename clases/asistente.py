
from time import sleep, time as timenow
from sys import exit

from clases.utils import *
from clases.audio_driver import *
from clases.google_driver import *
from clases.selenium_driver import *

from config import USER, PASSWORD

class Asistente():
    def __init__(self):
        """
        Este método inicializa la clase Asistente estableciendo las credenciales de usuario, la URL e iniciando el SeleniumDriver. Luego intenta iniciar sesión en la interfaz de chat de OpenAI. Si el inicio de sesión falla, imprime un mensaje de error y sale.

        Atributos:
        USER : str
        El correo electrónico del usuario para el inicio de sesión en el chat de OpenAI.
        PASSWORD : str
        La contraseña del usuario para el inicio de sesión en el chat de OpenAI.
        url : str
        La URL de la interfaz de chat de OpenAI.
        uc : SeleniumDriver
        Una instancia de la clase SeleniumDriver para controlar el navegador web.

        Retorna:
        Ninguno
        """
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.url = "https://chat.openai.com"
        print(f'{azul}Iniciando Selenium Drivers...{gris}')
        # Carga el Driver del Navegador
        self.uc = SeleniumDriver()
        login = self.login_openai() # Login
        print()
        if not login:
            print(f'\33[K{rojo}INICIO FALLIDO{gris}')
            exit()

    def login_openai(self):
        """
        Esta función intenta iniciar sesión en la interfaz de chat de OpenAI utilizando las credenciales de usuario proporcionadas. Primero navega a la URL especificada, luego realiza el proceso de inicio de sesión ingresando el correo electrónico y la contraseña del usuario. Después del proceso de inicio de sesión, verifica si el inicio de sesión fue exitoso comprobando la presencia de un elemento específico.

        Parámetros:
        Ninguno

        Retorna:
        bool: Devuelve True si el inicio de sesión fue exitoso, False en caso contrario.
        """
        print(f'\33[K{azul}Cargando Asistente...\n{gris}')  
        self.uc.Driver.get(self.url)
        self.uc.Driver.wait.load_start(timeout=2)
        #Login desde Cero
        if self.uc.Driver.ele('css:[data-testid="login-button"]',timeout=2):
            for i in range(5):
                try:
                    self.uc.Driver.ele('css:[data-testid="login-button"]').click()
                    self.uc.Driver.ele('css:social-logo').click()
                except:
                    pass
                try:
                    self.uc.Driver.ele('css:input[type="email"]',timeout=5).input(self.USER)
                    self.uc.Driver.ele('css:#identifierNext').click()
                except:
                    pass
                try:
                    self.uc.Driver.ele('css:input[type="password"]',timeout=5).input(self.PASSWORD)
                    self.uc.Driver.ele('css:#passwordNext').click()
                except:
                    pass

        login = self.comprobar_login()
        # Verifica si se pudo logear correctamente
        if login:
            return login
        else:
            print(f'\33[K{azul}COOKIES: {rojo}FALLIDO{gris}')

    def comprobar_login(self, tmpo=10):
        """
        Esta función verifica si el usuario ha iniciado sesión correctamente en la interfaz de chat de OpenAI. Intenta localizar un elemento específico en la página para verificar el estado de inicio de sesión. Si el inicio de sesión es exitoso, devuelve True. De lo contrario, devuelve False.

        Parámetros:
        tmpo (int, opcional): El tiempo máximo (en segundos) para esperar a que se complete el inicio de sesión. Por defecto es 3 segundos.

        Retorna:
        bool: Devuelve True si el inicio de sesión es exitoso, False en caso contrario.
        """
        login = False

        for i in range(tmpo):
            try:
                self.uc.Driver.ele('css:[data-testid="profile-button"]',timeout=5)
                self.uc.Driver.ele('css:#prompt-textarea').click()
                login = True
                break
            except:
                pass
            try:
                if self.uc.Driver.ele('tx=session has expired'):
                    cursor_arriba()
                    print(f'\33[K{amarillo}LA SESSION HA EXPIRADO{gris}')
                    print()
                    break
            except:
                pass
            cursor_arriba()
            print(f'\33[K{gris}Comprobando Login... {i}{gris}')
            sleep(1)
            
        cursor_arriba()
        print('\33[K')
        cursor_arriba(2)
        return login

    def ultima_conversacion(self):
        """
        Esta función intenta hacer clic en el botón "Historial" en la interfaz de usuario para acceder a la última conversación. Si no se encuentra el botón "Historial" dentro del tiempo de espera especificado, imprime un mensaje indicando que no se encontró la última conversación.

        Retorna:
        Ninguno
        """
        try:
            self.uc.Driver.ele('tx=Historial',  timeout=5).click()            
        except:
            print(f'\33[K{amarillo}No se encontro Ultima Conversacion{gris}')

        
    def chatear(self, prompt = None):
        if prompt:
            """
            Esta función simula una conversación con un modelo de IA enviando un mensaje inicial o pregunta y recibiendo una respuesta.

            Parámetros:
            prompt (str, opcional): El mensaje inicial o pregunta que se enviará al modelo de IA. Si no se proporciona, la función devolverá None.

            Retorna:
            str: La respuesta generada por el modelo de IA. Si no se proporciona ningún mensaje, la función devolverá None.
            """
            # Intruduce texto en el promp o textbox
            self.uc.Driver.ele('#:prompt-textarea').input(prompt)
            self.uc.Driver.ele('css:[data-testid="send-button"]').click()
            respuesta = ''
            sleep(0.5)
            # Generando las respuestas
            inicio = timenow()
            while True:
                # Obtener el último elemento markdown y su texto
                markdown = self.uc.Driver.eles('css:.markdown',timeout=0.5)
                if markdown:
                    respuesta = markdown[-1].text            
                # Verificar si el botón de "Stop generating" todavía está presente
                boton_stop = self.uc.Driver.ele('css:[data-testid="stop-button"]', timeout=0.5)
                if not boton_stop and respuesta:
                    break  # Salir del bucle si el botón no está presente y ya hay respuesta generada            
                # Calcular el tiempo transcurrido
                segundos = int(timenow() - inicio)
                if segundos > 0:                
                    print(f'\33[K{azul2}Generando respuesta... {gris}{segundos} segundos ({len(respuesta)} caracteres{gris})')
                    sleep(1)
                    # Mantener el cursor en la misma línea
                    cursor_arriba()              
            try:   
                if segundos:
                    print(f'\33[K{magenta}Respuesta generada en... {blanco}{segundos} {magenta}segundos{gris}')
            except:
                pass            
            # Esperar antes de devolver la respuesta final
            sleep(2)
            # Devolver la respuesta completa
            markdown = self.uc.Driver.eles('css:.markdown', timeout=1)
            return markdown[-1].text
        else:
            return None
    
    def buscar_texto_en_navegador(self, texto_a_buscar):
        """
        Esta función busca un texto específico en el navegador web utilizando Google.

        Parámetros:
        texto_a_buscar (str): El texto que se va a buscar. La función espera que la entrada esté en el formato "to_google <texto_a_buscar>".

        Retorna:
        Ninguno: La función no devuelve ningún valor. Imprime un mensaje de error si ocurre una excepción durante la búsqueda.

        Excepciones:
        Exception: Si ocurre un error durante la búsqueda, se captura y se imprime un mensaje de error.
        """
        try: 
            texto_filtrado = texto_a_buscar.split("to_google ", 1)
            GoogleDriver.buscar(text = texto_filtrado[1])              
        except:
            print("Ocurrió un error en la busqueda...")