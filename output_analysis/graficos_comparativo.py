import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Diccionario con tus escenarios y sus respectivos archivos
escenarios_archivos = {
    "Rotonda": "rotonda_base/resultados_TA.csv",
    "Semaforo": "Semaforo_interseccion/resultados_TA.csv",
    "Desnivel": "interseccion_puente/resultados_TA.csv",
    "Doble rotonda elevada": "doble_rotonda_puente/resultados_TA.csv"
}
resumen_total = []
kpis = ["dpi", "max_cola_norte", "max_cola_sureste1", "max_cola_sureste2", "throughput", "pvc"]
for nombre_esc, archivo in escenarios_archivos.items():
    ruta = f"{archivo}"
    df = pd.read_csv(ruta)
    n = len(df)

    for kpi in kpis:
        data = df[kpi]
        mean = data.mean()
        std = data.std(ddof=1) # sample std
        # Intervalo de confianza 95% con t-student
        alpha = 0.05
        t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
        margin = t_crit * (std / np.sqrt(n))
        
        resumen_total.append({
            "Escenario": nombre_esc,
            "KPI": kpi,
            "mean": mean,
            "std": std,
            "ci_lower": mean - margin,
            "ci_upper": mean + margin
        })

df_comparativo = pd.DataFrame(resumen_total)

# Esto te permite ver, por ejemplo, todos los DPI juntos
for escenario in escenarios_archivos.keys():
    print(f"Tabla para escenario: {escenario.upper()}")
    print(df_comparativo[df_comparativo['Escenario'] == escenario])

def graficar_kpi(kpi_nombre, titulo_y):
    subset = df_comparativo[df_comparativo['KPI'] == kpi_nombre]
    
    plt.figure(figsize=(10, 6))
    
    # Calculamos el error para las barras
    errores = [subset['mean'] - subset['ci_lower'], subset['ci_upper'] - subset['mean']]
    
    plt.errorbar(subset['Escenario'], subset['mean'], yerr=errores, 
                 fmt='o', capsize=10, markersize=5, elinewidth=2, color='RED')
    
    plt.title(f'Comparación de {kpi_nombre.upper()} con Intervalos de Confianza (95%)', fontsize=12)
    plt.ylabel(titulo_y)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Llamás a la función para los KPIs que quieras comparar
graficar_kpi('dpi', 'Segundos de Demora')
graficar_kpi('pvc', 'Porcentaje de viajes completados')