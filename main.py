from gurobipy import GRB, Model
from gurobipy import quicksum
import pandas as pd
import numpy as np

model = Model()
model.setParam("TimeLimit", 1800)

# ------------------- Conjuntos -------------------
I = range(0, 45) # Filas de posiciones de estanques
J = range(0, 45) # Columnas de posiciones de estanques
S = range(0, 105) # Sectores
E = range(0, 6) # Tipos de estanques
C = range(0, 5) # Categorias de camiones

# ------------------- Variables -------------------
# x[i, j, e] = Si el estanque en la posición (i, j) es de tipo e
x = model.addVars(I, J, E, vtype=GRB.BINARY, name="z")

# w[i, j, s] = Si el estanque en la posición (i, j) le suministra al sector s
w = model.addVars(I, J, S, vtype=GRB.BINARY, name="w")

# q[i, j, s] = Cantidad de agua que le suministra el estanque en la posición (i, j) al sector s
q = model.addVars(I, J, S, vtype=GRB.INTEGER, name="q")

# y[i, j, c] = Cantidad de camiones del tipo c que se envían al estanque en la posición (i, j)
y = model.addVars(I, J, C, vtype=GRB.INTEGER, name="y")

# n[i, j, c] = Si el camión del tipo c se envía al estanque en la posición (i, j)
n = model.addVars(I, J, C, vtype=GRB.BINARY, name="n")

model.update()

# ------------------- Parámetros -------------------------

# dijs distancia
distancias = pd.read_csv('parametros/distancias_estanques.csv')
dijs = {}

for index, row in distancias.iterrows():
    sector = row['Sector']
    fila = row['Fila']
    columna = row['Columna']
    distancia = row['Distancia']
    clave = (fila, columna, sector)

    dijs[clave] = distancia

# ce costo modelo estanque
ce = [1141567, 1815226, 2509080, 3919801, 5903205, 4774875]

# ps poblacion sector
poblaciones = pd.read_csv('parametros/poblacion_sector.csv', header=None).iloc[0].to_numpy()
ps = {i: poblaciones[i] for i in range(len(poblaciones))}

# m presupuesto
m = 7280000000

# l demanda de agua por persona
l = 172

# n_s ponderador sector

# kij si no se puede hacer estanque
validos = pd.read_csv('parametros/validez.csv')

kij = {}

for index, row in validos.iterrows():
    fila = row['Fila']
    columna = row['Columna']
    validez = row['Validez']
    clave = (fila, columna)
    
    kij[clave] = validez


# ve volumen estanque
ve = [10000, 15000, 20000, 30000, 35000, 40000]

# t costo fijo camion
t = 150000

# cc costo de camion c

# vc volumen de camion

# pijc si el camion c puede ir al estanque i, j

# M un numero muy grande


# ------------------- Restricciones ----------------------



# borrar esto
d_ijs = 1
n_s = 1

# ------------------- Función objetivo -------------------
funcion_objetivo = quicksum(w[i, j, s] * n_s * d_ijs for s in S for i in I for j in J)
model.setObjective(funcion_objetivo, GRB.MINIMIZE)



