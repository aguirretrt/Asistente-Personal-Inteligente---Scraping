#!/bin/bash

# Verificar si Python está en PATH
if ! command -v python3 &> /dev/null; then
  echo "Python no está en PATH. Asegúrate de que esté instalado correctamente."
  exit 1
fi

# Obtener la versión instalada de Python
python3 --version 2>&1 | grep -oP 'Python\s*\K\d+\.\d+\.\d+' > version.txt
read version_instalada < version.txt

# Comparar versiones
version_requerida="3.11"
IFS=. read -ra arr_instalada <<< "$version_instalada"
IFS=. read -ra arr_requerida <<< "$version_requerida"

if [[ "${arr_instalada[0]}" -ge "${arr_requerida[0]}" && \
      "${arr_instalada[1]}" -ge "${arr_requerida[1]}" ]]; then
  echo "Versión de Python correcta o superior: $version_instalada"

  # Función para instalar librerías
  install_libs() {
    pip install -r requirements.txt --break-system-packages || { echo "Error al instalar las librerías."; exit 1; }
    echo "Librerías instaladas correctamente."
  }

  install_libs

  # Crear y ejecutar el script RunAsistente.sh
  touch RunAsistente.sh
  echo "#!/bin/bash" > RunAsistente.sh
  echo "clear" > RunAsistente.sh
  echo "python3 main.py" >> RunAsistente.sh
  chmod +x RunAsistente.sh
  ./RunAsistente.sh

else
  echo "Versión de Python incorrecta. Se requiere al menos Python $version_requerida."
fi