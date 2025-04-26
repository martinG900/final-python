import json
from pathlib import Path

class Pais:
    '''Clase que representa los países del juego. Tiene asociadas su
    nombre, el número de ejércitos en él y los objetos Pais limítrofes'''

    with open(Path()/'data'/'limites.json') as f:
        limitrofes=json.load(f)

    def __init__(self,nombre):
        self.nombre=nombre
        self.ejercitos=0
        self.limitrofes=[Pais(i) for i in Pais.limitrofes[nombre]]
        self.jugador=None