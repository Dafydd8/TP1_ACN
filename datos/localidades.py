import csv
f = open('base_microdatos_bsas.csv', 'r', encoding='utf-8-sig')
#f_out = open('base_microdatos_buses.csv', 'w', encoding='utf-8-sig')

localidades_presentes = set()
for line in csv.DictReader(f):
    localidades_presentes.add(line['localidad_destino'])

localidades_list = list(localidades_presentes)
localidades_list.sort()

print(localidades_list)
print(len(localidades_presentes))
f.close()

