import csv

edades_intervalos = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 84]

edades = {
    "nueva aurora": [], "recreo": [], "forestal": [], "chorrillos": [],
    "viña oriente": [], "miraflores": [], "santa inés": [], "plan": [],
    "achupallas": [], "gómez carreño": [], "reñaca alto": [], "reñaca": [],
    "rezagados": [], "total comunal": []
}

with open('fuentes/edad_sectores.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i, key in enumerate(edades.keys(), start=1):
            edades[key].append(int(row[i]))


ponderadores_sector_grande = {
    "nueva aurora": 0, "recreo": 0, "forestal": 0, "chorrillos": 0,
    "viña oriente": 0, "miraflores": 0, "santa inés": 0, "plan": 0,
    "achupallas": 0, "gómez carreño": 0, "reñaca alto": 0, "reñaca": 0,
    "rezagados": 0, "total comunal": 0
}

for key in edades.keys():
    if key != "total comunal":
        suma_edad = 0
        suma_total = 0
        for i in range(len(edades_intervalos)):
            suma_edad += edades_intervalos[i] * edades[key][i]
            suma_total += edades[key][i]

        ponderadores_sector_grande[key] = suma_edad/suma_total
    else:
        total_comunal = 0
        suma_comunal = 0
        for i in range(len(edades_intervalos)):
            total_comunal += edades_intervalos[i] * edades[key][i]
            suma_comunal += edades[key][i]

        ponderadores_sector_grande[key] = total_comunal/suma_comunal


for key in ponderadores_sector_grande.keys():
    ponderadores_sector_grande[key] = round(ponderadores_sector_grande[key] / ponderadores_sector_grande["total comunal"], 4)


sectores = []

for i in range(105):
    
    if i < 19 or i == 21:
        sectores.append(ponderadores_sector_grande["reñaca"])

    elif  19 <= i <= 20 or i == 22 or 26 <= i <= 27 or 31 <= i <= 32:
        sectores.append(ponderadores_sector_grande["reñaca alto"])

    elif i == 23 or i == 28:
        sectores.append(ponderadores_sector_grande["gómez carreño"])

    elif i in [33, 39, 45, 46, 50, 51, 75, 85] or 55 <= i <= 58 or 64 <= i <= 66:
        sectores.append(ponderadores_sector_grande["plan"])

    elif i in [34, 40]:
        sectores.append(ponderadores_sector_grande["santa inés"])
      
    elif i in [35, 36, 41, 42, 48, 49, 53, 54, 62, 70]:
        sectores.append(ponderadores_sector_grande["achupallas"])

    elif i in [63, 81, 73, 83]:
        sectores.append(ponderadores_sector_grande["recreo"])

    elif i in [47, 52, 60, 68, 59, 67, 76, 86]:
        sectores.append(ponderadores_sector_grande["miraflores"])

    elif i in [61,69] or 77 <= i <= 80 or 87 <= i <= 90:
        sectores.append(ponderadores_sector_grande["viña oriente"])

    elif i in [91, 92, 96, 97]:
        sectores.append(ponderadores_sector_grande["nueva aurora"])
    
    elif i in [95, 100]:
        sectores.append(ponderadores_sector_grande["chorrillos"])

    elif i in [74,84,93,94,98,99,101,102,104]:
        sectores.append(ponderadores_sector_grande["forestal"])

    else:
        sectores.append(ponderadores_sector_grande["rezagados"])

print(sectores)

with open('parametros/ponderadores_sector.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow([i for i in range(len(sectores))])

    writer.writerow(sectores)