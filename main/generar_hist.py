import numpy as np
import matplotlib.pyplot as plt


def histograma(data, bins=10, title="Histograma de Distribucion", xlabel="Intervalos", ylabel="Frecuencia", bin_color="lightgreen", edgecolor="black"):
    
    # Crear el histograma
    plt.hist(data, bins=bins, edgecolor=edgecolor, color=bin_color)

    # Establecer el título y las etiquetas de los ejes
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    positions = np.linspace(min(data), max(data), bins+1)
    plt.xticks(positions)


    # Mostrar el gráfico
    plt.show()
    