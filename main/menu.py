import os
import sys

sys.path.append(os.getcwd())

from soporte import clear_console, wait_for_enter
import sub_menu_dist

while True:
    # clear_console()
    print("-- Opciones --")
    print("1 - Distribución uniforme(A,B)")
    print("2 - Distribución normal")
    print("3 - Distribución exponencial")
    print("0 - Salir ")

    try:
        
        opc = int(input("\nIngrese su opción: "))
        
        if opc not in [1, 2, 3, 0]:
            print("\nIngrese un valor dentro de las opciones...")
            print("\nPresione enter para continuar...")
            wait_for_enter()
        
        elif opc == 1:
            clear_console()
            print(" -- Distribución Uniforme --")
            sub_menu_dist.menu_uniforme()
            print("\nPresione enter para continuar...")
            wait_for_enter()
            clear_console()
        
        elif opc == 2:
            clear_console()
            print(" -- Distribución Normal --")
            sub_menu_dist.menu_normal()
            print("\nPresione enter para continuar...")
            wait_for_enter()
            clear_console()
        
        elif opc == 3:
            clear_console()
            print(" -- Distribución Exponencial --")
            sub_menu_dist.menu_exponencial()
            print("\nPresione enter para continuar...")
            wait_for_enter()
            clear_console()
        
        elif opc == 0:
            clear_console()
            print("Gracias por utilizar el código")
            print("\nPresione enter para finalizar...")
            wait_for_enter()
            clear_console()
            break
    
    except ValueError:
        print("Opción no válida. Por favor ingrese un número entero.")
        wait_for_enter()