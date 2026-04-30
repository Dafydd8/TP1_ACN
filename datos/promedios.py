import promedio_por_direccion

anios = []
for i in range(2019, 2025):
    anios.append(i)

dicts = []

for anio in anios:
    filename = f'base_microdatos_bsas_{anio}.csv'
    f = open(filename, 'r', encoding='utf-8-sig')
    promedios = promedio_por_direccion.get_promedio_por_trayecto(f)
    dicts.append(promedios)
    f.close()

promedios_recorridos = {}
for dict in dicts:
    for recorrido in dict:
        if not recorrido in promedios_recorridos:
            promedios_recorridos[recorrido] = 0
        promedios_recorridos[recorrido] += dict[recorrido]

for recorrido in promedios_recorridos:
    promedios_recorridos[recorrido] = promedios_recorridos[recorrido] / 6

print(promedios_recorridos)