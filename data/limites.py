import matplotlib.pyplot as plt
from pathlib import Path
import json
import numpy as np

#Abrir las cartas para obtener la lista de países

with open(Path()/'data'/'cartas.json','r',encoding='utf-8') as f:
    paises=json.load(f)

#Convertir lista de países en diccionario para añadir sus limítrofes

regiones={}

for a in paises.values():
    for b in a:
        regiones[b]=[]

#Abrir coordenadas de países para comparar su cercanía

with open(Path('.')/'data'/'country_coordinates.json','r',encoding='utf-8') as f:
    coords=json.load(f)

#Las coordenadas en y están invertidas, porque se consideró la esquina superior derecha como el origen.
#Se soluciona haciendo y=1226-y, donde 1226 es el alto del teg.jpg

for a in coords.values():
    a[1]=1226-a[1]

#Hallar los países limítrofes usando un radio elegido arbitrariamente y ajustando según
#la necesidad

dist=150

for a in coords.keys():
    for b in coords.keys():
        r=np.linalg.norm(np.array(coords[b])-np.array(coords[a]))
        if r<dist and r>0:
            regiones[a].append(b)

#Añadiendo los países al documento limites_preliminar.json. Luego se añaden los países limítrofes
#que el programa no detectó en el archivo limites.json

with open(Path()/'data'/'limites_preliminar.json','w',encoding='utf-8') as f:
    obj=json.dump(regiones,f,indent=4,ensure_ascii=False)

#Graficando las coordenadas de los países

'''x=[]
y=[]

for a in coords.values():
    x.append(a[0])
    y.append(a[1])

plt.plot(x,y,'o')
plt.show()'''
