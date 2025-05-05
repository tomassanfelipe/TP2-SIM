from generar_numeros import generar_numeros

def procesar_uniforme(n_string, a_string, b_string):
    n = int(n_string)
    a = int(a_string)
    b = int(b_string)
    
    if n <= 0 or n > 1000000:
        raise ValueError("La cantidad de muestras debe ser mayor que cero y hasta 1000000.")

    if a >= b:
        raise ValueError("El valor A debe ser menor que el valor B.")
    return generar_numeros("Uniforme", n, (a, b))

def procesar_normal(n_string, media_string, desviacion_string):
    n = int(n_string)
    media = int(media_string)
    desviacion = int(desviacion_string)
    
    if n <= 0 or n > 1000000:
        raise ValueError("La cantidad de muestras debe ser mayor que cero y hasta 1000000.")

    if desviacion <= 0:
        raise ValueError("La desviación estándar debe ser mayor que cero.")    
    return generar_numeros("Normal", n, (media, desviacion))

def procesar_exponencial(n_string, media_string):
    n = int(n_string)
    media = int(media_string)
    
    if n <= 0 or n > 1000000:
        raise ValueError("La cantidad de muestras debe ser mayor que cero y hasta 1000000.")

    if media <= 0:
        raise ValueError("La media debe ser mayor que cero.")
    lambd = 1 / media
    return generar_numeros("Exponencial", n, (lambd,))