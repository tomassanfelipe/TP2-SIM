import pandas as pd
import numpy as np

def get_class(d, clases):
    for i in range(len(clases)-1):
        if  clases[i] < d <= clases[i+1]:      
            return i+1
    
        elif d <= clases[i]: 
            return i
# ----------------------------------------POSIBLE MEJORA ------------------------------------------
# def get_class(d, clases):
#     for i in range(len(clases) - 1):
#         if clases[i] < d <= clases[i + 1]:
#             return i
#     return None
# --------------------------------------------------------------------------------------------------
        
def generar_tabla(datos, kclases): # el kclases va poder ser 10, 15, 20 o 25
    # aegura que los datos sean tipo float
    datos = np.array(datos, dtype=float)
    
    minimo = round(np.min(datos), 4)
    maximo = round(np.max(datos), 4)
    rango = maximo - minimo
    intervalo = round(rango / kclases, 4)
    
    clases = [minimo + intervalo * i for i in range(kclases)]
    clases_visto = [f"({clases[i]:.2f}; {clases[i+1]:.2f})" for i in range(kclases-1)] # mejora el formato para que se vea ordenado
    
    frecuencias = [0] * kclases
    for d in datos:
        pos_clase = get_class(d, clases)
        if pos_clase is not None:
            frecuencias[pos_clase] += 1
        else: 
            print(f"Valor fuera de rango: {d}")
    
    tabla = []
    for i in range(kclases - 1):
        rango = clases_visto[i]
        frecuencia = frecuencias[i]
        marca_clase = (clases[i] + clases[i+1]) / 2
        tabla.append((rango, frecuencia, marca_clase))

    df = pd.DataFrame(tabla, columns=["Rango", "Frecuencia", "Marca de Clase"])
    
    return df.to_string(index=False) 