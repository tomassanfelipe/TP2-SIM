from uniforme import uniforme
from normal import normal
from exponencial import exponencial

def generar_numeros(distribucion, n, params):
    if distribucion == 'Uniforme':
        a, b = params
        numeros = [uniforme(a, b) for _ in range(n)]

    elif distribucion == 'Exponencial':
        lambd = params[0]
        numeros = [exponencial(lambd) for _ in range(n)]

    elif distribucion == 'Normal':
        media, v = params
        numeros = []
        for _ in range(n // 2):
            n1, n2 = normal(media, v)
            numeros.extend([n1, n2])
        if n % 2 != 0:
            n1, _ = normal(media, v)
            numeros.append(n1)

    return numeros