import json
from pathlib import Path
from random import shuffle
from modules.cartas import Mazo
from modules.jugador import Jugador
import numpy as np

# Funciones


def tiros(m: int, jugs):
    """Función a la que se le pasa una lista de objetos Jugador. Hace que todos
    estos jugadores lancen los dados y compara sus resultados. Indica quienes
    son los m jugadores con los mayores resultados. La función tiene en cuenta los empates
    """

    ganadores = []

    while True:

        # Todos los jugadores de la lista tiran dados

        for a in jugs:
            a.tirar()

        # Los jugadores se ordenan según sus dados en orden descendente

        jugs.sort(key=lambda x: x.dado, reverse=True)
        valores = [i.dado for i in jugs]

        resultados = list({6, 5, 4, 3, 2, 1} & set(valores))
        resultados.sort(reverse=True)

        # Se chequean quienes califican para ganar y se repiten los tiros para
        # los que empataron

        for a in resultados:
            if valores.count(a) == m - len(ganadores):
                ganadores.extend(jugs[: valores.count(a)])
                return ganadores
            elif valores.count(a) > m - len(ganadores):
                jugs = jugs[: valores.count(a)].copy()
                break
            else:
                ganadores.extend(jugs[: valores.count(a)])
                jugs = jugs[valores.count(a) :]


# INICIALIZACIÓN

# Abrir las cartas. Se considera al 0 de la lista como el tope del mazo


with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
    cartas = json.load(f)

mazo = Mazo(cartas)
mazo.mezclar()

# Crear jugadores

numJ = 4

J = [Jugador(f"José {i+1}") for i in range(numJ)]

# Repartir paí­ses por jugador. Recordar que pueden sobrar dos cartas si jugadores=3,4,6

if numJ in [2, 5]:
    mano = len(mazo) // numJ
    [i.robar(mano, mazo) for i in J]
else:
    mano = (len(mazo) - 2) // numJ
    [i.robar(mano, mazo) for i in J]

    # Introducir el tiro de dados y las dos cartas extra

    [j.robar(1, mazo) for j in tiros(2, J)]

# Cada jugador añade 1 ejército a sus países

[j.reclamar(1, j.cartas.mazo) for j in J]

# Quitar las cartas de las manos de los jugadores y resetear el mazo de cartas

[j.soltar(j.cartas.mazo, mazo) for j in J]

mazo.mezclar()

# Cada jugador añade 5 ejércitos repartidos entre sus paí­ses. Pueden
# reclamar la misma región más de una vez

[i.reclamos(5,list(i.territorios.keys())) for i in J]

# Cada jugador añade 3 ejércitos repartidos entre sus paí­ses

[i.reclamos(3,list(i.territorios.keys())) for i in J]
