import csv
import random

input_file = './parametros/validez.csv'
output_file = './parametros/validez_copia.csv'

with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
  reader = csv.reader(infile)
  writer = csv.writer(outfile)
  
  for row in reader:
    fila, columna, validez = row
    if validez == '1':
      validez = '0'
    else:
      validez = '1'
    writer.writerow([fila, columna, validez])