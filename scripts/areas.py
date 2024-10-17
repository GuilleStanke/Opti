def cuadrado_valido(punto, esquina_inferior_izquierda, esquina_superior_derecha):
    x = punto[0]
    y = punto[1]
    x1, y1 = esquina_inferior_izquierda
    x2, y2 = esquina_superior_derecha
    
    # Verificar si el punto está dentro del rango de las coordenadas del cuadrado
    if x1 <= x <= x2 and y1 <= y <= y2:
        return True
    return False

def calcular_area(x1, y1, x2, y2, x3, y3):

    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def triangulo_valido(punto, vertice1, vertice2, vertice3):

    x = punto[0]
    y = punto[1]
    x1, y1 = vertice1
    x2, y2 = vertice2
    x3, y3 = vertice3
    
    # Área del triángulo original (ABC)
    area_total = calcular_area(x1, y1, x2, y2, x3, y3)
    
    # Áreas de los triángulos formados con el punto (PBC, PAC, PAB)
    area1 = calcular_area(x, y, x2, y2, x3, y3)
    area2 = calcular_area(x1, y1, x, y, x3, y3)
    area3 = calcular_area(x1, y1, x2, y2, x, y)
    
    # Si la suma de las áreas es igual al área total, el punto está dentro
    if area_total == area1 + area2 + area3:
        return True
    return False

