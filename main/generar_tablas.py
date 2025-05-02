import pandas as pd
import numpy as np

def get_class_index(d, classes):

    for i in range(len(classes)-1):

        # si esta en el siguiente intervalo
        if  classes[i] < d <= classes[i+1]:      #     2.1 < d <= 3.4
            return i+1
        
        # En caso de que el valor d este en la actual (sirve para la primer clase)
        elif d <= classes[i]:    #  <  4
            return i
        # Si no esta en el siguiente, ni en el actual, pasa a la siguiente iteracion
        
def generate_frequency_table(data, k_classes):
    # Asegurarse de que los datos son flotantes
    data = np.array(data, dtype=float)
    
    # Calcular valores mínimos, máximos y el rango
    minimo = round(np.min(data), 4)
    maximo = round(np.max(data), 4)
    rango = maximo - minimo
    intervalo = round(rango / k_classes, 4)
    
    # Crear las clases (intervalos)
    clases = [minimo + intervalo * i for i in range(k_classes)]
    clases_bonito = [f"({clases[i]:.2f}; {clases[i+1]:.2f})" for i in range(k_classes-1)]
    
    # Contar las frecuencias
    contador_frecuencias = [0] * k_classes
    for d in data:
            index = get_class_index(d, clases)
            if index is not None:
                contador_frecuencias[index] += 1
    
    tabla = []
    for i in range(k_classes - 1):
        rango = clases_bonito[i]
        frecuencia = contador_frecuencias[i]
        marca_clase = (clases[i] + clases[i+1]) / 2
        tabla.append((rango, frecuencia, marca_clase))
    
    # Convertir la tabla a un DataFrame para mostrarla
    df = pd.DataFrame(tabla, columns=["Rango", "Frecuencia", "Marca de Clase"])
    
    return df.to_string(index=False)