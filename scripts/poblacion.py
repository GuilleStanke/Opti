import csv

poblacion_por_sector_grande = {}


with open('fuentes/poblacion_sectores_grandes.csv', mode='r', newline='') as file:
    reader = csv.reader(file)

    sectores = next(reader)

    poblaciones = next(reader)

    poblacion_por_sector_grande = {sectores[i].strip().replace('"', '').lower(): int(poblaciones[i]) for i in range(len(sectores))}


print(poblacion_por_sector_grande)

sectores_por_sector = {
  "nueva aurora": 4, "reñaca": 20, "plan": 15, "viña oriente": 10,
  "recreo": 4, "forestal": 9, "santa inés": 2, "chorrillos": 2, 
  "achupallas": 10, "gómez carreño": 2, "reñaca alto": 7, "miraflores": 8
}

sectores = []

for i in range(105):
    
    if i < 19 or i == 21:
        sectores.append(poblacion_por_sector_grande["reñaca"] / sectores_por_sector["reñaca"])

    elif  19 <= i <= 20 or i == 22 or 26 <= i <= 27 or 31 <= i <= 32:
        sectores.append(poblacion_por_sector_grande["reñaca alto"] / sectores_por_sector["reñaca alto"])

    elif i == 23 or i == 28:
        sectores.append(poblacion_por_sector_grande["gómez carreño"] / sectores_por_sector["gómez carreño"])

    elif i in [33, 39, 45, 46, 50, 51, 75, 85] or 55 <= i <= 58 or 64 <= i <= 66:
        sectores.append(poblacion_por_sector_grande["plan"] / sectores_por_sector["plan"])

    elif i in [34, 40]:
        sectores.append(poblacion_por_sector_grande["santa inés"] / sectores_por_sector["santa inés"])
      
    elif i in [35, 36, 41, 42, 48, 49, 53, 54, 62, 70]:
        sectores.append(poblacion_por_sector_grande["achupallas"] / sectores_por_sector["achupallas"])

    elif i in [63, 81, 73, 83]:
        sectores.append(poblacion_por_sector_grande["recreo"] / sectores_por_sector["recreo"])

    elif i in [47, 52, 60, 68, 59, 67, 76, 86]:
        sectores.append(poblacion_por_sector_grande["miraflores"] / sectores_por_sector["miraflores"])

    elif i in [61,69] or 77 <= i <= 80 or 87 <= i <= 90:
        sectores.append(poblacion_por_sector_grande["viña oriente"] / sectores_por_sector["viña oriente"])

    elif i in [91, 92, 96, 97]:
        sectores.append(poblacion_por_sector_grande["nueva aurora"] / sectores_por_sector["nueva aurora"])
    
    elif i in [95, 100]:
        sectores.append(poblacion_por_sector_grande["chorrillos"] / sectores_por_sector["chorrillos"])

    elif i in [74,84,93,94,98,99,101,102,104]:
        sectores.append(poblacion_por_sector_grande["forestal"] / sectores_por_sector["forestal"])

    else:
        sectores.append(0)

print(sectores)

with open('parametros/poblacion_sectores.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(sectores)