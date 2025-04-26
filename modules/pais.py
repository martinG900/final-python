import json
from pathlib import Path


class Pais:
    """Clase que representa los países del juego. Tiene asociadas su
    nombre, el número de ejércitos en él, los objetos Pais limítrofes
    y el objeto Jugador que posee este país"""

    with open(Path() / "data" / "limites.json", encoding="utf-8") as f:
        limitrofes = json.load(f)

    paises = []

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.ejercitos = 0
        self.limitrofes = None
        self.jugador = None
        if self not in Pais.paises:
            Pais.paises.append(self)

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, pais2):
        return self.nombre == pais2.nombre

    @classmethod
    def limites(cls):

        for a in cls.paises:
            a.limitrofes = [cls(i) for i in cls.limitrofes[a.nombre]]