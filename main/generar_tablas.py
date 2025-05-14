import pandas as pd
import numpy as np

def get_class(d, clases): # es para que incluya un numero si es igual al limite superior de la clase
    for i in range(len(clases) - 1):
        if clases[i] <= d < clases[i + 1] or np.isclose(d, clases[i + 1]):
            return i
    if d == clases[-1]:
        return len(clases) - 2
    return None
        
def generar_tabla(datos, kclases): 
    datos = np.array(datos, dtype=float)
    
    minimo = np.min(datos)
    maximo = np.max(datos)
    rango = maximo - minimo
    intervalo = rango / kclases

    clases = [minimo + intervalo * i for i in range(kclases + 1)]
    clases_visto = [f"({clases[i]:.2f}; {clases[i+1]:.2f})" for i in range(kclases)]
    
    frecuencias = [0] * kclases
    for d in datos:
        pos_clase = get_class(d, clases)
        if pos_clase is not None:
            frecuencias[pos_clase] += 1
        else: 
            print(f"Valor fuera de rango: {d}")
    
    tabla = []
    for i in range(kclases):
        rango = clases_visto[i]
        frecuencia = frecuencias[i]
        marca_clase = round((clases[i] + clases[i+1]) / 2, 4)
        tabla.append((rango, frecuencia, marca_clase))

    df = pd.DataFrame(tabla, columns=["Rango", "Frecuencia", "Marca de Clase"])
    return df.to_string(index=False)

# para testear la tabla
# datos = [
# ]

# kclases = 

# print(generar_tabla(datos, kclases))