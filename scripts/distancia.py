import math
import pandas as pd

def calcular_distancias(puntos_referencia, lista_puntos, DISTX, DISTY):

    distancias = []

    # Iterar sobre los puntos de referencia
    for punto_ref in puntos_referencia:

        x1, y1 = punto_ref


        # Iterar sobre los otros puntos y calcular la distancia para cada punto de referencia
        for punto in lista_puntos:
            lista = [puntos_referencia.index(punto_ref)]
            if isinstance(punto, (tuple, list)):
                x2, y2 = punto
            else:
                raise ValueError(f"Formato de punto inesperado: {punto}")

            # Calcular la distancia ponderada
            distancia = math.sqrt(((x2 * DISTX) - x1*DISTX) ** 2 + ((y2 * DISTY) - y1*DISTY) ** 2)
            distancia_redondeada = round(distancia, 4)# Redondear a 4 decimales
            lista.append(punto[1])
            lista.append(punto[0])
            lista.append(distancia_redondeada)

            distancias.append(lista)

    columnas = ["Sector"] + ["Fila"] + ["Columna"] + ["Distancia"]
    # Crear un DataFrame con las distancias
    df_distancias = pd.DataFrame(distancias, columns = columnas)

    # Exportar el DataFrame a un archivo Excel
    df_distancias.to_csv("parametros/distancias_estanques.csv", index=False)
    
    print("Las distancias se han exportado correctamente a 'distancias_estanques.csv'.")


