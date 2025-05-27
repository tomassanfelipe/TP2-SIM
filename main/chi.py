from scipy.stats import chi2, norm
import math
import numpy as np
import pandas as pd

def prueba_chi_cuadrado(datos, distribucion, intervalos=10):
    avisos = []
    n = len(datos)

    if n < 30:
        avisos.append(f"Tamaño de muestra pequeño (n={n})")

    if intervalos > n / 5:
        intervalos = max(1, int(math.sqrt(n)))
        avisos.append(f"Intervalos ajustados a {intervalos} debido al tamaño de muestra.")

    valor_minimo, valor_maximo = min(datos), max(datos)
    ancho = (valor_maximo - valor_minimo) / intervalos
    fo, limites_inferiores, limites_superiores = [], [], []

    for i in range(intervalos):
        inf = valor_minimo + i * ancho
        sup = valor_minimo + (i + 1) * ancho
        if i == intervalos - 1:
            sup = valor_maximo + 1e-4  # incluir el valor máximo
        limites_inferiores.append(inf)
        limites_superiores.append(sup)
        conteo = sum(inf <= x < sup for x in datos)
        fo.append(conteo)

    fe = []

    if distribucion == "Uniforme":
        fe = [n / intervalos] * intervalos
        m = 0

    elif distribucion == "Exponencial":
        lambd = 1 / np.mean(datos)
        for i in range(intervalos):
            inf, sup = max(limites_inferiores[i], 0), limites_superiores[i]
            prob = math.exp(-lambd * inf) - math.exp(-lambd * sup)
            fe.append(prob * n)
        m = 1

    elif distribucion == "Normal":
        media = np.mean(datos)
        desv = np.std(datos, ddof=0)
        for i in range(intervalos):
            inf, sup = limites_inferiores[i], limites_superiores[i]
            prob = norm.cdf(sup, media, desv) - norm.cdf(inf, media, desv)
            fe.append(prob * n)
        m = 2

    else:
        raise ValueError("Seleccione uina distribucion adecuada.")

    # Agrupar intervalos con FE < 5
    i = 0
    while i < len(fe):
        if fe[i] < 5 and len(fe) > 1:
            j = i + 1 if i < len(fe) - 1 else i - 1
            if j < i:
                i, j = j, i
            fo[i] += fo.pop(j)
            fe[i] += fe.pop(j)
            limites_superiores[i] = limites_superiores.pop(j)
            limites_inferiores.pop(j)
            avisos.append(f"Se agruparon intervalos {i} y {j} por frecuencia esperada < 5.")
            i = max(0, i - 1)
        else:
            i += 1

    # Cálculos
    diferencia = [fo - fe for fo, fe in zip(fo, fe)]
    diferencia_cuadrado = [(d) ** 2 for d in diferencia]
    c = [(d2 / fe if fe > 0 else 0) for d2, fe in zip(diferencia_cuadrado, fe)]
    cAc = np.cumsum(c).tolist()
    chi = cAc[-1]
    k = len(fe)
    gl = max(1, k - 1 - m)
    valor_critico = chi2.ppf(0.95, gl)
    conclusion = "No se rechaza" if chi <= valor_critico else "Se rechaza"

    # Crear tabla clara
    tabla = pd.DataFrame({
        "Intervalo": [f"[{round(limites_inferiores[i], 4)}, {round(limites_superiores[i], 4)})" for i in range(k)],
        "FO": fo,
        "FE": [round(fe, 2) for fe in fe],
        #"FO - FE": [round(d, 2) for d in diferencia],
        #"(FO - FE)^2": [round(d2, 2) for d2 in diferencia_cuadrado],
        "C": [round(ci, 4) for ci in c],
        "C(AC):": [round(ca, 4) for ca in cAc]
    })

    # Resumen detallado
    txt = (
        f"--- Prueba Chi-Cuadrado ---\n"
        f"Distribución evaluada: {distribucion}\n"
        f"N: {n}\n"
        f"Mínimo: {valor_minimo:.4f}\n"
        f"Máximo: {valor_maximo:.4f}\n"
        f"Número de intervalos: {k}\n"
        f"Grados de libertad: {gl}\n"
        f"Chi calculado: {chi:.4f}\n"
        f"Valor crítico (α = 0.05): {valor_critico:.4f}\n"
        f"Conclusión: {conclusion} la hipótesis de que los datos siguen una distribución {distribucion}.\n"
    )

    if avisos:
        txt += "\n--- Avisos ---\n" + "\n".join(avisos)

    return tabla, txt