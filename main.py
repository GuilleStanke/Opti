from gurobipy import GRB, Model
from gurobipy import quicksum
import pandas as pd
import numpy as np

model = Model()
model.setParam("TimeLimit", 1800)
# model.setParam("NumericFocus", 3) # ayuda a mitigar problemas numéricos


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

#z[i, j, e] = Modelo del estanque "e" en posicion (i, j)
z = model.addVars(I, J, E, vtype=GRB.BINARY, name="z")

model.update()

# ------------------- Parámetros -------------------------

# d_ijs distancia
distancias = pd.read_csv('parametros/distancias_estanques.csv')
d_ijs = {}

for index, row in distancias.iterrows():
    sector = row['Sector']
    fila = row['Fila']
    columna = row['Columna']
    distancia = row['Distancia']
    clave = (fila, columna, sector)

    d_ijs[clave] = distancia

# ce costo modelo estanque
c_e = [1141567, 1815226, 2509080, 3919801, 5903205, 4774875]

# p_s poblacion sector
poblaciones = pd.read_csv('parametros/poblacion_sectores.csv', header=None).iloc[0].to_numpy()
p_s = {i: poblaciones[i] for i in range(len(poblaciones))}

# m presupuesto
m = 7280000000

# l demanda de agua por persona
l = 1

# n_s ponderador sector
ponderadores = pd.read_csv('parametros/ponderadores_sector.csv', header=None).iloc[0].to_numpy()
n_s = {i: ponderadores[i] for i in range(len(ponderadores))}

# k_ij si no se puede hacer estanque
validos = pd.read_csv('parametros/validez.csv')

k_ij = {}

for index, row in validos.iterrows():
    fila = row['Fila']
    columna = row['Columna']
    validez = row['Validez']
    clave = (fila, columna)
    
    k_ij[clave] = validez

# ve volumen estanque
v_e = [10000, 15000, 20000, 30000, 35000, 40000]

# t costo fijo camion
t = 150000

# c_c costo de camion c
c_c = [90000, 130000, 165000, 225000, 300000]

# v_c volumen de camion c
v_c = [1000, 5000, 10000, 20000, 30000]

# p_ijc si el camion c puede ir al estanque i, j
validos = pd.read_csv('parametros/validez_camiones_bueno.csv')

p_ijc = {}

for index, row in validos.iterrows():
    fila = int(row['Fila'])
    columna = int(row['Columna'])
    validez = int(row['Validez'])
    camion = int(row['Camion'])
    clave = (fila, columna, camion)
    
    p_ijc[clave] = validez

# M un numero muy grande
M = 1000000000000

# ------------------- Restricciones ----------------------

# 1) Se debe respetar el presupuesto:
model.addConstr((quicksum(quicksum(quicksum((x[i, j, e]*c_e[e]) for e in E) for j in J) for i in I)) + (quicksum(quicksum(quicksum((y[i, j, c]*(c_c[c] + t)) for c in C) for j in J) for i in I)) <= m, name='R1')
print("R1")

# 2) Si no se construye un estanque en (i, j), entonces (i, j) no puede ser un punto de suministro:
for j in J:
    for i in I:
        for s in S:
            model.addConstr(quicksum(x[i, j, e] for e in E) >= w[i, j, s], name='R2')
print("R2")

# 3) Solo se pueden construir estanques en lugares específicos:
for j in J:
    for i in I:
        model.addConstr(quicksum(x[i, j, e] for e in E) <= 1 - k_ij[(i, j)], name='R3')
print("R3")

# 4) Se tiene que cumplir la demanda por sector:
for s in S:
    model.addConstr(quicksum(quicksum(q[i, j, s] for j in J) for i in I) >= p_s[s]*l, name='R4')
print("R4")

# 5) La cantidad de agua de un estanque que se destina los sectores no puede superar la capacidad máxima del estanque:
for j in J:
    for i in I:
        model.addConstr(quicksum((x[i, j, e]*v_e[e]) for e in E) >= quicksum(q[i, j, s] for s in S), name='R5')
print("R5")

# 6) Si el estanque en (i, j) no suministra a (s), entonces la parte destinada del estanque en (i, j) a (s)  es 0:
for j in J:
    for i in I:
        for s in S:
            model.addConstr(quicksum((w[i, j, s] * v_e[e]) for e in E) >= q[i, j, s], name='R6')
print("R6")

# 7) Solo hay 1 tipo de estanque (e)  por estanque:
for j in J:
    for i in I:
        model.addConstr(1 >= quicksum(x[i, j, e] for e in E), name='R7')
print("R7")

# 8) La cantidad de agua total que suministra un estanque a los sectores no puede superar a la cantidad de agua que le suministran los camiones al estanque.
for j in J:
    for i in I:
        model.addConstr(quicksum((y[i, j, c]*v_c[c]) for c in C) >= quicksum(q[i, j, s] for s in S), name='R8')
print("R8")

# 9) El camión no va, si no hay estanque en  (i,j).
for j in J:
    for i in I:
        model.addConstr(quicksum(y[i, j, c] for c in C) <= quicksum(M * x[i, j, e] for e in E), name='R9')
print("R9")

# 10) Si se decide no enviar un camión a (i,j) se envían cero camiones:           
for j in J:
    for i in I:
        for c in C:
            model.addConstr(y[i, j, c] <= M * n[i, j, c], name='R10')
print("R10")

# 11) No se envían camiones donde no pueden acceder:
for j in J:
    for i in I:
        for c in C:
            model.addConstr(n[i, j, c] <= p_ijc[(i, j, c)], name='R11')
print("R11")

# 12) La cantidad de agua que lleva un camion tipo (c) al estanque en (i,j)no puede superar la capacidad del estanque tipo (e).
for j in J:
    for i in I:
        model.addConstr(quicksum((y[i, j, c]*v_c[c]) for c in C) <= quicksum((x[i, j, e]*v_e[e]) for e in E), name='R2')
print("R12")



# Nuevas
for j in J:
    for i in I:
        model.addConstr(quicksum((x[i, j, e]) for e in E) <= quicksum(w[i, j, s] for s in S), name='R13')
print("R13")

for j in J:
    for i in I:
        for c in C:
            model.addConstr(quicksum(x[i, j, e] for e in E) >= n[i, j, c], name='R14')
print("R14")


# ------------------- Función objetivo -------------------
funcion_objetivo = quicksum(w[i, j, s] * n_s[s] * d_ijs[(i, j, s)] for s in S for i in I for j in J)
model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()

# # Detectar infeasibilidad si el modelo es infactible
# if model.Status == GRB.INFEASIBLE:
#     print("El modelo es infactible. Generando el archivo .ilp para diagnóstico...")
#     model.computeIIS()
#     model.write("model.ilp")
#     print("Archivo 'model.ilp' generado con las restricciones problemáticas.")

# Tiempo de ejecucion
tiempo_ejecucion = model.Runtime
# Valor objetivo:
valor_objetivo = model.ObjVal

print("----------------------------")
print(f"Valor onjetivo: {valor_objetivo}")
print("----------------------------")

num_sol = 0
print("Variables:\n")
cantidad_x = 0
for i in I:
    for j in J:
        for e in E:
            if x[i, j, e].x != 0:
                print(f'X_({i, j, e}): {x[i, j, e].x}')
                num_sol += 1
                cantidad_x += 1
print(f'Cantidad de x: {cantidad_x}')

for i in I:
    for j in J:
        for s in S:
            if w[i, j, s].x != 0 and q[i, j, s].x != 0:
                print(f'W_({i, j, s}): {w[i, j, s].x}   --   Q_({i, j, s}): {q[i, j, s].x}')
                num_sol += 1



for i in I:
    for j in J:
        suma_w = 0
        suma_q = 0
        if x[i, j, 5].x == 0:
            for s in S:
                suma_w += w[i, j, s].x
                suma_q += q[i, j, s].x
            if suma_w != 0 or suma_q != 0:
                print(f'Estanque en ({i}, {j}) esta mal')


# si xije es 1, la suma de W es mayor o igual a 1, imprimir casos conrtrarios
for i in I:
    for j in J:
        suma_w = 0
        if x[i, j, 5].x == 1:
            for s in S:
                suma_w += w[i, j, s].x
            if suma_w < 1:
                print(f'Estanque en ({i}, {j}) esta mal')

for i in I:
    for j in J:
        suma_n = 0
        suma_y = 0
        if x[i, j, 5].x == 1:
            for c in C:
                suma_n += n[i, j, c].x
                suma_y += y[i, j, c].x
            if suma_n < 1 or suma_y < 1:
                print(f'Estanque en ({i}, {j}) esta mal')

for i in I:
    for j in J:
        suma_n = 0
        suma_y = 0
        if x[i, j, 5].x == 0:
            for c in C:
                suma_n += n[i, j, c].x
                suma_y += y[i, j, c].x
            if suma_n > 0 or suma_y > 0:
                print(f'Estanque en ({i}, {j}) esta mal')

        

# for i in I:
#     for j in J:
#         for s in S:
#             if q[i, j, s].x != 0:
#                 print(f'Q_({i, j, s}): {q[i, j, s].x}')
#                 num_sol += 1

# for i in I:
#     for j in J:
#         for c in C:
#             if y[i, j, c].x != 0:
#                 print(f'Y_({i, j, c}): {y[i, j, c].x}')
#                 num_sol += 1

# for i in I:
#     for j in J:
#         for c in C:
#             if n[i, j, c].x != 0:
#                 print(f'N_({i, j, c}): {n[i, j, c].x}')
#                 num_sol += 1


print(f"Tiempo: {tiempo_ejecucion}")

print(f'num soluciones: {num_sol}')
