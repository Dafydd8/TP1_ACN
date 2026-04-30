import csv
import datetime

def filtrar_por_fecha(fecha_min:datetime.datetime, fecha_max:datetime.datetime, filename_in, filename_out):
    f = open(filename_in, 'r', encoding='utf-8-sig')
    reader = csv.DictReader(f, delimiter=',')
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    f_out = open(filename_out, 'w', encoding='utf-8-sig')
    header = "fecha,localidad_origen,provincia_origen,pais_origen,localidad_destino,provincia_destino,pais_destino,par_origen_destino,ruta_clasificacion,descripcion,asientos,pasajeros\n"
    f_out.write(header)
    for line in reader:
        date = datetime.datetime.strptime(line['fecha'], '%Y-%m-%d')
        if date < fecha_max and date > fecha_min:
            if line['provincia_destino'] in {'Buenos Aires', 'Ciudad Autónoma De Buenos Aires'}:
                f_out.write(','.join(line.values()) + '\n')
        
    f_out.close()
    f.close()
