from generar_numeros import generar_numeros

# Procesar distribución Uniforme
def procesar_uniforme(n_str, a_str, b_str):
    n = int(n_str)
    a = int(a_str)
    b = int(b_str)

    if a >= b:
        raise ValueError("El valor inferior A debe ser menor que el valor superior B.")
    
    return generar_numeros("Uniforme", n, (a, b))

# Procesar distribución Normal
def procesar_normal(n_str, media_str, desviacion_str):
    n = int(n_str)
    media = int(media_str)
    desviacion = int(desviacion_str)

    if desviacion <= 0:
        raise ValueError("La desviación estándar debe ser mayor que cero.")
    
    return generar_numeros("Normal", n, (media, desviacion))

# Procesar distribución Exponencial
def procesar_exponencial(n_str, media_str):
    n = int(n_str)
    media = int(media_str)

    if media <= 0:
        raise ValueError("La media debe ser mayor que cero.")
    
    lambd = 1 / media
    return generar_numeros("Exponencial", n, (lambd,))