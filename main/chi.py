from scipy.stats import chi2, norm
import math
import numpy as np
import pandas as pd

def prueba_chi_cuadrado(datos, distribucion, intervalos=10):
    advertencias = []
    n = len(datos)

    if n < 30:
        advertencias.append(f"Tamaño de muestra pequeño (n={n})")

    if intervalos > n / 5:
        intervalos = max(1, int(math.sqrt(n)))
        advertencias.append(f"Intervalos ajustados a {intervalos} debido al tamaño de muestra.")

    min_val, max_val = min(datos), max(datos)
    ancho = (max_val - min_val) / intervalos
    frec_obs, limites_inf, limites_sup = [], [], []

    for i in range(intervalos):
        inf = min_val + i * ancho
        sup = min_val + (i + 1) * ancho
        if i == intervalos - 1:
            sup = max_val + 1e-4  # incluir el valor máximo
        limites_inf.append(inf)
        limites_sup.append(sup)
        conteo = sum(inf <= x < sup for x in datos)
        frec_obs.append(conteo)

    frec_esp = []

    if distribucion == "Uniforme":
        frec_esp = [n / intervalos] * intervalos
        m = 0

    elif distribucion == "Exponencial":
        lambd = 1 / np.mean(datos)
        for i in range(intervalos):
            inf, sup = max(limites_inf[i], 0), limites_sup[i]
            prob = math.exp(-lambd * inf) - math.exp(-lambd * sup)
            frec_esp.append(prob * n)
        m = 1

    elif distribucion == "Normal":
        media = np.mean(datos)
        desv = np.std(datos, ddof=0)
        for i in range(intervalos):
            inf, sup = limites_inf[i], limites_sup[i]
            prob = norm.cdf(sup, media, desv) - norm.cdf(inf, media, desv)
            frec_esp.append(prob * n)
        m = 2

    else:
        raise ValueError("Seleccione uina distribucion adecuada.")

    # Agrupar intervalos con FE < 5
    i = 0
    while i < len(frec_esp):
        if frec_esp[i] < 5 and len(frec_esp) > 1:
            j = i + 1 if i < len(frec_esp) - 1 else i - 1
            if j < i:
                i, j = j, i
            frec_obs[i] += frec_obs.pop(j)
            frec_esp[i] += frec_esp.pop(j)
            limites_sup[i] = limites_sup.pop(j)
            limites_inf.pop(j)
            advertencias.append(f"Se agruparon intervalos {i} y {j} por frecuencia esperada < 5.")
            i = max(0, i - 1)
        else:
            i += 1

    # Cálculos
    diferencia = [fo - fe for fo, fe in zip(frec_obs, frec_esp)]
    diferencia_cuadrado = [(d) ** 2 for d in diferencia]
    c = [(d2 / fe if fe > 0 else 0) for d2, fe in zip(diferencia_cuadrado, frec_esp)]
    cAc = np.cumsum(c).tolist()
    chi = cAc[-1]
    k = len(frec_esp)
    gl = max(1, k - 1 - m)
    valor_critico = chi2.ppf(0.95, gl)
    conclusion = "No se rechaza" if chi <= valor_critico else "Se rechaza"

    # Crear tabla clara
    tabla = pd.DataFrame({
        "Intervalo": [f"[{round(limites_inf[i], 4)}, {round(limites_sup[i], 4)})" for i in range(k)],
        "FO": frec_obs,
        "FE": [round(fe, 2) for fe in frec_esp],
        #"FO - FE": [round(d, 2) for d in diferencia],
        #"(FO - FE)^2": [round(d2, 2) for d2 in diferencia_cuadrado],
        "C": [round(ci, 4) for ci in c],
        "C(AC):": [round(ca, 4) for ca in cAc]
    })

    # Resumen detallado
    resumen = (
        f"---------- Chi-Cuadrado ----------\n"
        f"Distribución evaluada: {distribucion}\n"
        f"N: {n}\n"
        f"Mínimo: {min_val:.4f}\n"
        f"Máximo: {max_val:.4f}\n"
        f"Número de intervalos: {k}\n"
        f"Grados de libertad: {gl}\n"
        f"Chi calculado: {chi:.4f}\n"
        f"Valor crítico (α = 0.05): {valor_critico:.4f}\n"
        f"Conclusión: {conclusion} la hipótesis de que los datos siguen una distribución {distribucion}.\n"
    )

    if advertencias:
        resumen += "\n---------- Observaciones ----------\n" + "\n".join(advertencias)

    return tabla, resumen