from DrissionPage import ChromiumPage, ChromiumOptions
from sbvirtualdisplay import Display

from config import VISIBLE

class SeleniumDriver():       
    def __init__(self, visible=VISIBLE):   
        """
        Inicializar una instancia de SeleniumDriver.

        Esta clase es responsable de gestionar la pantalla virtual, las opciones del navegador y la instancia del Selenium WebDriver.

        Parámetros:
        visible (bool): Una bandera que indica si la pantalla virtual debe ser visible. El valor predeterminado es el valor de la constante VISIBLE.

        Retorna:
        Ninguno
        """
        self.virtual_display = Display(visible=visible, size=(740, 470))
        self.virtual_display.start()

        self.opciones = ChromiumOptions().headless(False)
        self.opciones.set_argument("--blink-settings=imagesEnabled,false")
        self.opciones.set_argument("--disable-gpu")
        self.opciones.set_argument("--force-device-scale-factor=0.70")

        self.Driver = ChromiumPage(self.opciones) 
        self.Driver.set.window.full()
        
    def __del__(self):
        self.Driver.quit()
        self.virtual_display.stop()
    