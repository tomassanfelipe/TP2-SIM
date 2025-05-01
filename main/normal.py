import math
import random

def normal(media, desv):
    rnd1 = random.random()
    rnd2 = random.random()
    n1 = (((math.sqrt(-2 * math.log(rnd1))) * math.cos(2 * math.pi * rnd2)) * desv) + media
    n2 = (((math.sqrt(-2 * math.log(rnd1))) * math.sin(2 * math.pi * rnd2)) * desv) + media
    return n1, n2


""" --------------------------------------------------------   VALIDACIONES --------------------------------------------------- """

def validar_muestra():
    while True:
        try:
            
            n = int(input("Ingrese el valor de la muestra (hasta 1.000.000 y mayor que 30): "))
            if n > 30 and n <= 1000000:
                break
            else:
                print("La muestra debe estar entre 30 y 1000000, por favor ingrese un valor válido.")

        except ValueError:
            print("Por favor ingrese un número entero válido.")

    return n


def validar_intervalo_a_b():
    while True:
        try:
            a = float(input("Ingrese el valor inferior del intervalo (A): "))
            b = float(input("Ingrese el valor superior del intervalo (B): "))
            
            if a == 0 and b == 1:
                print("El valor de a y b no puede ser 0 y 1 respectivamente. Por favor ingrese nuevamente los valores.")
            else:
                if a < b:
                    return a, b
                else:
                    print("El valor de 'A' debe ser menor que el valor de 'B'. Por favor ingrese nuevamente los valores.")

        except ValueError:
            print("Por favor ingrese valores numéricos válidos.")


def seleccionar_intervalos_histograma():
    while True:
        try:
            intervalos = int(input("Seleccione el número de intervalos (10, 15, 20, 25): "))
            if intervalos in [10, 15, 20, 25]:
                return intervalos
            else:
                print("Por favor seleccione un número de intervalos válido.")
        except ValueError:
            print("Por favor ingrese un número entero.")


def validar_media():
    while True:
        try:
            media = float(input("Ingrese el valor de la media: "))
            if media > 0:
                return media
            else:
                print("La media debe ser un número positivo. Inténtelo de nuevo.")
        except ValueError:
            print("Ingrese un valor numérico para la media.")
            
"""----------------------------------------------------------   VALIDACIONES --------------------------------------------------- """           