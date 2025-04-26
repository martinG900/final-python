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
        self.jugador = None
        if self not in Pais.paises:
            Pais.paises.append(self)
            self.limitrofes = [Pais(i) for i in Pais.limitrofes[self.nombre]]

    def reforzar(self, n: int):
        """Función que añade n ejércitos al objeto Pais"""

        self.ejercitos += n

    def incorporar(self, jugador):
        """Función que hace que el objeto Pais quede ligado a un
        jugador. Se le entrega un objeto Jugador"""

        self.jugador = jugador

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    # Añadí eq para que dos objetos Pais sean iguales si tienen el
    # mismo nombre

    def __eq__(self, pais2):
        return self.nombre == pais2.nombre
