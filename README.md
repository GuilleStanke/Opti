# Opti
# Instrucciones de Organización

Para mantener una estructura clara y ordenada en tu proyecto, sigue estas directrices:

## Ubicación de Archivos

- **Scripts Python**: Los scripts que se utilizan para generar parámetros en formato CSV deben ubicarse en la carpeta `scripts`. Esto facilita la localización y ejecución de los scripts necesarios.
- **Archivos de Datos**: Todos los archivos de datos, ya sean en formato CSV, Excel u otros, deben almacenarse en la carpeta `fuentes`. Esto asegura que todos los datos de entrada estén centralizados en un solo lugar.
- **Archivos CSV de Parámetros**: Los archivos CSV que contienen parámetros específicos deben guardarse en la carpeta `parametros`. Esto permite un acceso rápido y organizado a los parámetros necesarios para el proyecto.

## Formato de los Archivos CSV

Para asegurar la consistencia y facilidad de uso de los archivos CSV, sigue estas pautas:

- **Columnas por Tipo de Dato**: Cada tipo de dato debe estar en su propia columna. Por ejemplo, para las distancias:
En vez de tener el valor de distancia en la interseccion de (i,j) y s, hacer cada dato en cada columna:


| sector | fila | columna | distancia |
|--------|------|---------|-----------|
| 0      | 0    | 0       | 12.5      |
| 1      | 0    | 1       | 8.3       |
| 2      | 0    | 2       | 15.7      |
| 3      | 0    | 3       | 9.1       |
Es decir el csv quedaria como:
```
sector,fila,columna,distancia
0,0,0,12.5
1,0,1,8.3
2,0,2,15.7
3,0,3,9.1
```

Siguiendo estas instrucciones, podrás mantener tu proyecto organizado y facilitar el manejo de datos y scripts.