import pandas as pd

# Cambiá el nombre si tu archivo se llama distinto
df = pd.read_csv("resultados_parametros.csv")

# Cola máxima global de cada corrida
df["max_cola_global"] = df[
    ["max_cola_norte", "max_cola_sureste1", "max_cola_sureste2"]
].max(axis=1)

# Cola promedio entre accesos
df["cola_promedio_accesos"] = df[
    ["max_cola_norte", "max_cola_sureste1", "max_cola_sureste2"]
].mean(axis=1)

# Agrupar por combinación de tiempos semafóricos
resumen = (
    df.groupby(["duracion11", "duracion56"])
    .agg(
        dpi_mean=("dpi", "mean"),
        dpi_std=("dpi", "std"),
        max_cola_global_mean=("max_cola_global", "mean"),
        max_cola_global_max=("max_cola_global", "max"),
        cola_promedio_mean=("cola_promedio_accesos", "mean"),
        max_cola_norte_mean=("max_cola_norte", "mean"),
        max_cola_sureste1_mean=("max_cola_sureste1", "mean"),
        max_cola_sureste2_mean=("max_cola_sureste2", "mean"),
        throughput_mean=("throughput", "mean"),
        pvc_mean=("pvc", "mean"),
        n=("id", "count")
    )
    .reset_index()
)

# Ranking simple:
# Queremos minimizar dpi y colas, maximizar throughput y pvc.
# Para poder comparar, normalizamos todo entre 0 y 1.
def minmax(s):
    if s.max() == s.min():
        return pd.Series(0, index=s.index)
    return (s - s.min()) / (s.max() - s.min())

resumen["score_dpi"] = minmax(resumen["dpi_mean"])
resumen["score_cola"] = minmax(resumen["max_cola_global_mean"])
resumen["score_cola_prom"] = minmax(resumen["cola_promedio_mean"])
resumen["score_throughput"] = 1 - minmax(resumen["throughput_mean"])
resumen["score_pvc"] = 1 - minmax(resumen["pvc_mean"])

# Score final: menor es mejor
resumen["score_final"] = (
    0.35 * resumen["score_dpi"] +
    0.35 * resumen["score_cola"] +
    0.1 * resumen["score_cola_prom"] +
    0.1 * resumen["score_throughput"] +
    0.1 * resumen["score_pvc"]
)

ranking = resumen.sort_values("score_final")

print("Ranking de configuraciones semafóricas:")
print(
    ranking[
        [
            "duracion11",
            "duracion56",
            "dpi_mean",
            "max_cola_global_mean",
            "max_cola_global_max",
            "cola_promedio_mean",
            "throughput_mean",
            "pvc_mean",
            "score_final",
            "n"
        ]
    ]
)

mejor = ranking.iloc[0]

print("\nMejor combinación general:")
print(f"Duración RP11: {mejor['duracion11']} s")
print(f"Duración RP56: {mejor['duracion56']} s")
print(f"DPI promedio: {mejor['dpi_mean']:.2f}")
print(f"Cola máxima global promedio: {mejor['max_cola_global_mean']:.2f}")
print(f"Throughput promedio: {mejor['throughput_mean']:.2f}")
print(f"PVC promedio: {mejor['pvc_mean']:.4f}")

# Mejor específicamente por cola
mejor_colas = resumen.sort_values("max_cola_global_mean").iloc[0]

print("\nMejor combinación minimizando cola máxima promedio:")
print(f"Duración RP11: {mejor_colas['duracion11']} s")
print(f"Duración RP56: {mejor_colas['duracion56']} s")
print(f"Cola máxima global promedio: {mejor_colas['max_cola_global_mean']:.2f}")

# Guardar resumen ordenado
ranking.to_csv("ranking_configuraciones_semaforo.csv", index=False)