from uniforme import uniforme
from normal import normal
from exponencial import exponencial

def generar_numeros(distribucion, n, parametros):
    if distribucion == 'Uniforme':
        a, b = parametros
        numeros = [uniforme(a, b) for i in range(n)]

    elif distribucion == 'Exponencial':
        lambd = parametros[0]
        numeros = [exponencial(lambd) for i in range(n)]

    elif distribucion == 'Normal':
        media, desviacion = parametros
        numeros = []
        for i in range(n // 2): # con n//2 aseguro que se generen dos numeros por iteracion
            n1, n2 = normal(media, desviacion)
            numeros.extend([n1, n2])
        if n % 2 != 0:  # aca verifica que si no son pares
            n1, i = normal(media, desviacion) # genera un numero adicional
            numeros.append(n1) # solo agrega un valor de los dos que se generan 

    return numeros