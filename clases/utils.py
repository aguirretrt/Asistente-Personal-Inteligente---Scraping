
verde = '\33[1;32m'
verde2 = '\33[0;32m'
amarillo = '\33[1;33m'
amarillo2 = '\33[0;33m'
azul = '\33[1;36m'
azul2 = '\33[0;36m'
magenta = '\33[1;35m'
magenta2 = '\33[0;35m'
gris = '\33[0;37m'
gris2 = '\33[0;90m'
blanco = '\33[1;37m'
rojo = '\33[1;31m'
rojo2 = '\33[0;31m'
negro_gris = '\33[0;30;47m'
negro_blanco = '\33[0;30;107m'
negro_amarillo ='\33[0;30;103m'
negro_azul = '\33[0;30;106m'
negro_verde = '\33[0;30;102m'
blanco_azul = '\33[0;37;44m'
blanco_azul_parp = '\33[6;37;44m'

#Funcion para subir el cursor nL líneas en la terminal
def cursor_arriba(nL = 1):
    print(f'\33[{nL}A', end = '')


