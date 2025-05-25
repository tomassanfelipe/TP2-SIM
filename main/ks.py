from scipy.stats import norm
import math
import numpy as np
import pandas as pd

def prueba_ks(datos, distribucion, intervalos=None):
    datos = sorted(datos)
    n = len(datos)
    intervalos = intervalos if intervalos else int(math.sqrt(n))
    min_val, max_val = min(datos), max(datos)
    ancho = (max_val - min_val) / intervalos

    # Frecuencias observadas por intervalo
    frec_obs = [0] * intervalos
    for x in datos:
        idx = int((x - min_val) / ancho)
        idx = min(idx, intervalos - 1)
        frec_obs[idx] += 1

    # Probabilidades observadas y acumuladas
    Po = [fo / n for fo in frec_obs]
    PoAc = np.cumsum(Po).tolist()

    # Probabilidades esperadas y acumuladas
    Pe, PeAc, sup_limites = [], [], []
    
    intervalos_str = []
    for i in range(intervalos):
        lim_inf = min_val + i * ancho
        lim_sup = min_val + (i + 1) * ancho
        intervalos_str.append(f"[{lim_inf:.4f}, {lim_sup:.4f})")

    if distribucion == "Uniforme":
        for i in range(intervalos):
            sup = min_val + (i + 1) * ancho
            sup_limites.append(sup)
            peac = (sup - min_val) / (max_val - min_val) if max_val != min_val else 0
            PeAc.append(peac)
        Pe = [PeAc[0]] + [PeAc[i] - PeAc[i - 1] for i in range(1, intervalos)]

    elif distribucion == "Exponencial":
        lambd = 1 / np.mean(datos)
        for i in range(intervalos):
            sup = min_val + (i + 1) * ancho
            sup_limites.append(sup)
            peac = 1 - math.exp(-lambd * sup) if sup >= 0 else 0
            PeAc.append(peac)
        Pe = [PeAc[0]] + [PeAc[i] - PeAc[i - 1] for i in range(1, intervalos)]

    elif distribucion == "Normal":
        media = np.mean(datos)
        desv = np.std(datos, ddof=0)
        for i in range(intervalos):
            sup = min_val + (i + 1) * ancho
            sup_limites.append(sup)
            peac = norm.cdf(sup, media, desv)
            PeAc.append(peac)
        Pe = [PeAc[0]] + [PeAc[i] - PeAc[i - 1] for i in range(1, intervalos)]

    else:
        raise ValueError("Seleccione una distribucion adecuada")

    # Estadístico KS
    diferencias = [abs(poac - peac) for poac, peac in zip(PoAc, PeAc)]
    D = max(diferencias)

    # Valor crítico
    valor_critico = 1.36 / math.sqrt(n)  # α = 0.05 (para cualquier n)

    conclusion = "No se rechaza" if D <= valor_critico else "Se rechaza"
    resumen = f"--- Prueba KS ---\n"
    resumen += f"Distribución evaluada: {distribucion}\n"
    resumen += f"N: {n}\n"
    resumen += f"Estadístico KS = {D:.4f}\n"
    resumen += f"Valor crítico (α = 0.05): {valor_critico:.4f}\n"
    resumen += f"Conclusión: {conclusion} la hipótesis de que los datos siguen la distribución {distribucion}"

    # Tabla resumen
    tabla = pd.DataFrame({
        "Intervalo": intervalos_str,
        "FO.": frec_obs,
        "FE": [round(p * n) for p in Pe],
        "Po": [f"{p:.4f}" for p in Po],
        "Pe": [f"{p:.4f}" for p in Pe],
        "PoAc": [f"{p:.4f}" for p in PoAc],
        "PeAc": [f"{p:.4f}" for p in PeAc],
        "|PoAc - PeAc|": [f"{d:.4f}" for d in diferencias]
        #"MAX": ["<--" if d == D else "" for d in diferencias]
    })

    return tabla, resumen