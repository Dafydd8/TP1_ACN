import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

escenarios_archivos = {
    "Rotonda": "rotonda_base/resultados_TB.csv",
    "Semaforo": "Semaforo_interseccion/resultados_TB.csv",
    "Desnivel": "interseccion_puente/resultados_TB.csv",
    "Doble rotonda elevada": "doble_rotonda_puente/resultados_TB.csv"
}

kpis = ["dpi", "max_cola_norte", "max_cola_sureste1", "max_cola_sureste2", "throughput", "pvc"]
resumen_total = []

for nombre_esc, archivo in escenarios_archivos.items():
    df = pd.read_csv(archivo)
    n = len(df)
    
    for kpi in kpis:
        data = df[kpi]
        mean, std = data.mean(), data.std(ddof=1)
        
        t_crit = stats.t.ppf(1 - 0.05/2, df=n-1)
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

# Visualización de tablas por consola
for escenario in escenarios_archivos.keys():
    print(f"\n--- Escenario: {escenario.upper()} ---")
    print(df_comparativo[df_comparativo['Escenario'] == escenario])

def graficar_kpi(kpi_nombre, titulo_y):
    subset = df_comparativo[df_comparativo['KPI'] == kpi_nombre]
    plt.figure(figsize=(10, 6))
    
    errores = [subset['mean'] - subset['ci_lower'], subset['ci_upper'] - subset['mean']]
    
    plt.errorbar(subset['Escenario'], subset['mean'], yerr=errores,
                 fmt='o', capsize=10, markersize=6, elinewidth=2, color='RoyalBlue')
    
    plt.title(f'Comparación de {kpi_nombre.upper()} con Intervalos de Confianza (95%)', fontsize=12)
    plt.ylabel(titulo_y)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Gráficos individuales
graficar_kpi('dpi', 'Segundos de Demora')
graficar_kpi('throughput', 'Promedio de vehiculos por hora')
graficar_kpi('pvc', 'Porcentaje de viajes completados')

# Gráfico comparativo de Colas
colas_kpis = ['max_cola_norte', 'max_cola_sureste1', 'max_cola_sureste2']
df_colas = df_comparativo[df_comparativo['KPI'].isin(colas_kpis)]
escenarios_lista = df_colas['Escenario'].unique()
colores = ['#3F88C5', '#FFBA08', '#D00000']
offsets = [-0.2, 0.0, 0.2]

plt.figure(figsize=(12, 7))

for i, kpi in enumerate(colas_kpis):
    subset = df_colas[df_colas['KPI'] == kpi]
    x_coords = np.arange(len(escenarios_lista)) + offsets[i]
    yerr = [subset['mean'] - subset['ci_lower'], subset['ci_upper'] - subset['mean']]
    
    plt.errorbar(x_coords, subset['mean'], yerr=yerr, fmt='o', color=colores[i], 
                 label=kpi, capsize=8, markersize=8, elinewidth=2, 
                 markeredgecolor='black', alpha=0.9)

plt.title('Comparación de Colas Máximas con Intervalos de Confianza (95%)', fontsize=14, pad=15)
plt.ylabel('Cantidad de Vehículos')
plt.xticks(np.arange(len(escenarios_lista)), escenarios_lista)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(title='Ruta')
plt.tight_layout()
plt.show()