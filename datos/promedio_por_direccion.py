import csv
import datetime

localidades_norte = ['Avellaneda', 'Berazategui', 'Burzaco', 'Chascomus', 'Ciudad Autónoma De Buenos Aires', 'Ciudadela', 'Ezeiza', 'Florencio Varela', 'Ingeniero Budge', 'Junin', 'La Lucila', 'La Plata', 'Moron', 'Pablo Nogues', 'Pergamino', 'Rafael Castillo', 'San Justo', 'San Miguel', 'San Nicolas', 'San Pedro', 'Zarate']
localidades_corredor = ['Las Toninas', 'Mar De Ajó', 'Mar Del Tuyu', 'San Bernardo', 'Santa Teresita']
localidades_sur = ['Pinamar', 'Villa Gesell']


def get_promedio_por_trayecto(f):
    buses_por_trayecto_fecha:dict[tuple[str, str, datetime.datetime], int] = {}
    buses_por_trayecto = {}
    fechas_por_trayecto = {}

    for line in csv.DictReader(f):
        destino = line['localidad_destino']
        origen = line['localidad_origen']

        if destino in localidades_norte:
            destino = 'norte'
        elif destino in localidades_corredor:
            destino = 'corredor'
        elif destino in localidades_sur:
            destino = 'sur'
        else:
            continue

        if origen in localidades_norte:
            origen = 'norte'
        elif origen in localidades_corredor:
            origen = 'corredor'
        elif origen in localidades_sur:
            origen = 'sur'
        else:
            continue

        recorrido = (origen, destino)
        if recorrido in [('norte', 'norte'), ('corredor', 'corredor'), ('sur', 'sur'), ('corredor', 'sur'), ('sur', 'corredor')]:
            continue
        fecha = datetime.datetime.strptime(line['fecha'], '%Y-%m-%d')

        if (origen, destino, fecha) not in buses_por_trayecto_fecha:
            buses_por_trayecto_fecha[(origen, destino, fecha)] = 0
            if recorrido not in fechas_por_trayecto:
                fechas_por_trayecto[recorrido] = 0
            fechas_por_trayecto[recorrido] += 1
        buses_por_trayecto_fecha[(origen, destino, fecha)] += 1

        if recorrido not in buses_por_trayecto:
            buses_por_trayecto[recorrido] = 0
        buses_por_trayecto[recorrido] += 1

    promedio_por_trayecto = {trayecto: buses_por_trayecto[trayecto] / fechas_por_trayecto[trayecto] for trayecto in buses_por_trayecto}
    f.close()
    return promedio_por_trayecto