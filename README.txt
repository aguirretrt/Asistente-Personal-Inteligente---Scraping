Asistente Personal Inteligente basado en tecnicas de Scraping



* Esta aplicación es de código abierto y su uso está destinado exclusivamente a
  fines educativos, con el objetivo de fomentar el trabajo colaborativo y la 
  posibilidad de modificar y mejorar la herramienta de manera libre. Sin embargo,
  cualquier modificación o uso indebido de la aplicación es responsabilidad 
  exclusiva del usuario.



* Nota I.: este asistente utiliza como base la plataforma de IA de Chat Gpt,
  para loguearse debe tener una cuenta Google registrada, los datos de usuario
  y contraseña deben ser añadidos al archivo config.py.
  Para visualizar como es el proceso de inicialización puede modificar en el archivo config.py
  la opción de VISIBLE = True y luego cambiar a False.
  Para que el AVI recupere las conversaciones, en la barra lateral debe existir
  una sección con el nombre "Historial".

* Nota II.: para realizar modificaciones a su medida se recomienda tener conocimientos
  básicos de Python.

  
* Instalar python 3.11.4 o Mayor
* Instalar pip3
* Instalar Google Chrome
* Instalar NoiseTorch (opcional)

* Instalar librerias
  sudo apt install python3-pyaudio
  sudo apt-get install ffmpeg
  sudo apt-get install xvfb

* Intalar los paquetes del archivo requirements.txt
  pip3 install -r requirements.txt --break-system-packages

* Funcionalidad

  Para activar el asistente y que este reconozca que se le está dirigiendo un comando, 
  es necesario utilizar las palabras de activación que se encuentran en el archivo config.py.
  Estas palabras pueden personalizarse o ampliarse para incluir otras frases de su elección.
  Ejemplo de uso: Asistente quiero o Asistente dime, seguido de la instrucción deseada.

  En el archivo audio_driver.py se encuentran algunos comandos predefinidos para tareas
  específicas. Si tiene conocimientos de Python, puede agregar y personalizar otros comandos
  para realizar funciones particulares según sus necesidades.

  Tenga en cuenta que, si utiliza micrófono y audífonos, no tendrá inconvenientes al usar 
  el asistente. Sin embargo, si no los utiliza, deberá bajar un poco el volumen de salida 
  para evitar que el micrófono capture el audio de salida junto con su voz. Esto podría 
  impedir que el asistente entienda correctamente sus comandos. Para finalizar la 
  reproducción del audio, simplemente debe decir: Asistente quiero finalizar.

  Para finalizar la comunicación con el asistente, simplemente debe 
  decir: Asistente quiero finalizar.
