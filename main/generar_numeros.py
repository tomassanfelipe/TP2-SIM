from uniforme import uniforme
from normal import normal
from exponencial import exponencial

def generar_numeros(distribucion, n, parametros):
    if distribucion == 'Uniforme':
        a, b = parametros
        numeros = [round(uniforme(a, b), 4) for i in range(n)]

    elif distribucion == 'Exponencial':
        lambd = parametros[0]
        numeros = [round(exponencial(lambd), 4) for i in range(n)]

    elif distribucion == 'Normal':
        media, desviacion = parametros
        numeros = []
        for i in range(n // 2): # con n//2 aseguro que se generen dos numeros por iteracion
            n1, n2 = normal(media, desviacion)
            numeros.extend([round(n1, 4), round(n2, 4)])
        if n % 2 != 0:  # aca verifica que si no son pares
            n1, i = normal(media, desviacion) # genera un numero adicional
            numeros.append(round(n1, 4)) # solo agrega un valor de los dos que se generan 
            

    return numeros