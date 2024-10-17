from areas import cuadrado_valido, triangulo_valido
import pandas as pd


#Areas en las que es valido un estanque
cuadrados = [[(12, 0), (20, 12)], [(20, 4), (28, 8)], [(12, 12), (16, 16)], [(24, 16), (36, 36)], 
            [(4, 28), (24, 36)], [(4, 36), (20, 40)], [(0, 32), (4, 36)], [(16, 40), (20, 44)],
            [(24, 36), (28, 40)], [(36, 32), (40, 36)], [(8, 24), (16, 28)], [(12, 20), (20, 24)],
            [(36, 16), (40, 24)], [(40, 16), (44, 20)], [(32, 12), (36, 16)]]

triangulos = [[(20, 0), (20, 4), (24, 4)], [(16, 12), (20, 12), (20, 16)], [(36, 12), (40, 12), (36, 16)],
            [(32, 40), (36, 40), (36, 44)],[(12, 40), (12, 44), (16, 40)]]



#Creacion de estanques
estanques = []

for i in range(45):
    fila = []
    for j in range(45):
        fila.append([j, i])
    estanques.append(fila)

validos = []

i = 0
for fila in estanques:
    for estanque in fila:
        val = [estanque[1]]
        val.append(estanque[0])
        valido = False
        for cuadrado in cuadrados:
            if cuadrado_valido(estanque, cuadrado[0], cuadrado[1]):
                valido = True
                break
        for triangulo in triangulos:
            if triangulo_valido(estanque, triangulo[0], triangulo[1], triangulo[2]):
                valido = True
                break
        if valido: 
            val.append(1)
        else:
            val.append(0)
        validos.append(val)
    i += 1

columnas = ["Fila"] + ["Columna"] + ["Validez"]

df_validos = pd.DataFrame(validos, columns = columnas)

    # Exportar el DataFrame a un archivo Excel
df_validos.to_csv("parametros/validez.csv", index=False)

print("Las distancias se han exportado correctamente a 'validez.csv'.")


