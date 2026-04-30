import pandas as pd
import numpy as np
from scipy import stats

carpeta = input("Ingrese la carpeta donde se encuentra el archivo CSV: ")
filename = input("Ingrese el nombre del archivo CSV (con extensión): ")
ruta = f"../{carpeta}/{filename}"

df = pd.read_csv(ruta)

# Columnas KPI (sacamos id)
kpis = ["dpi", "max_cola_norte", "max_cola_sureste1", "max_cola_sureste2", "throughput", "pvc"]

n = len(df)

resultados = []

for kpi in kpis:
    data = df[kpi]
    
    mean = data.mean()
    std = data.std(ddof=1)  # sample std
    
    # Intervalo de confianza 95% con t-student
    alpha = 0.05
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    
    margin = t_crit * (std / np.sqrt(n))
    
    ci_lower = mean - margin
    ci_upper = mean + margin
    
    resultados.append({
        "KPI": kpi,
        "mean": mean,
        "std": std,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    })

resumen = pd.DataFrame(resultados)

print(resumen)