import json
from pathlib import Path

##Programa para chequear que los límites entre países se implementaron
#adecuadamente. No esencial para el código principal una vez chequeado
#que limites.json es correcto

with open(Path()/'data'/'limites.json',encoding='utf-8') as f:
    limites=json.load(f)

for a in list(limites.keys()):
    for b in limites[a]:
        if a in limites[b]:
            print(f'todo bien con {a}')
        else:
            print(f'problema en {a},{b}')