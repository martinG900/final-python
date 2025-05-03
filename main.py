import json
import random as rn
from pathlib import Path
from modules.cartas import Mazo
from modules.jugador import Jugador
from modules.pais import Pais
from modules.dibujar import dibujar


### DATOS
with open("data/country_coordinates.json", "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
    cartas = json.load(f)

# Colores que pueden tomar los jugadores
colores = ["cyan", "orange", "green", "red", "white", "pink"]

# Nombres que pueden tomar los jugadores
nombres = ["Pablo", "Yanina", "Tomás", "Horacio", "Omar", "Nahuel"]
rn.shuffle(nombres)


### INICIALIZACIÓN

nombres_paises = []
[nombres_paises.extend(i) for i in cartas.values()]

# Crear lista de objetos Pais con todos los países del juego
paises = [Pais(i) for i in nombres_paises]

# Definir los países limítrofes de cada país
Pais.definir_limitrofes()

# Crear objeto Mazo cuyas cartas son objetos Pais
mazo = Mazo(paises)

mazo.mezclar()

# Crear Mazo de descarte
descarte = Mazo([])

numero_jugadores = 6

# Lista de objetos Jugador
jugadores = [Jugador(i, j) for i, j in list(zip(nombres, colores))[:numero_jugadores]]

# Repartir cartas a todos los jugadores
if len(mazo) % numero_jugadores == 0:
    numero_cartas = len(mazo) // numero_jugadores
    [i.robar(numero_cartas, mazo) for i in jugadores]
else:
    numero_cartas = (len(mazo) - 2) // numero_jugadores
    [i.robar(numero_cartas, mazo) for i in jugadores]

    # Sobran dos cartas y jugadores compiten por estas
    [i.robar(1, mazo) for i in Jugador.tiros(2, jugadores)]

for i in jugadores:

    # Jugadores adquieren países y colocan un ejército en cada uno
    i.desplegar(1, i.cartas)

    # Jugadores devuelven sus cartas al mazo
    i.devolver(i.cartas, mazo)

    mazo.mezclar()

    # Jugadores despliegan ejércitos en sus países
    i.despliegues(5, [j for j in i.territorios])
    i.despliegues(3, [j for j in i.territorios])

# Orden en el que juegan jugadores
rn.shuffle(jugadores)

# Estado inicial del mapa
dibujar(paises, coordenadas)

### BUCLE DE JUEGO

victoria = False

for m in range(1000):  # O sino "while not victoria:"

    # Flujo para cada jugador
    for j in jugadores:

        # Revisar si jugador perdió y saltearlo
        if len(j.territorios) <= 0:
            jugadores.remove(j)
            continue

        ##FASE DE CANJE

        j.canjear(descarte)

        ##FASE DE ATAQUE

        # Realizar ataques un número aleatorio de veces
        for n in range(
            rn.randint((100 - j.reserva) // 20, ((100 - j.reserva) // 5) + 1)
        ):
            j.atacar()

        # Terminada la fase de ataque, el juguador pierde el país que
        # tenía como objetivo para conquistar, dado por la carta robada
        # en la fase de Llamado
        j.pais_objetivo(None)

        # Revisa condición de victoria
        if len(j.territorios) >= 50:
            victoria = True
            ganador = j

        ##FASE DE REAGRUPAMIENTO

        # Revisa si hay países que pueden movilizar tropas
        paises_movimiento = [i for i in j.mis_paises() if i.ejercitos > 1]

        if paises_movimiento:
            maximas_tropas = max([i.ejercitos for i in paises_movimiento])

            # Mueve tropas entre países propios un número aleatorio de
            # veces
            for m in range(rn.randint(2 * maximas_tropas, 4 * maximas_tropas + 1)):
                j.reagrupar()

        ##FASE DE LLAMADO

        # Fase solo ocurre si jugador conquistó al menos un país en este
        # turno
        if j.conquistador:

            # Jugador reinicia sus conquistas. Tiene que volver a
            # conquistar en el siguiente turno para entrar a esta fase
            j.sin_conquistas()

            j.robar(1, mazo)

            # Si carta es de país propio, lo refuerza. Si no, jugador
            # tiene un país objetivo para el siguiente turno
            if j.cartas[-1] in j.territorios:
                j.desplegar(2, [j.cartas[-1]])
            else:
                j.pais_objetivo(j.cartas[-1])

        # Si cartas del mazo se acaban, usar el descarte para rellenarlo
        if len(mazo) == 0:
            descarte.repartir(n=len(descarte), recipiente=mazo)

        ##FASE DE REFUERZO

        # Jugador distribuye refuerzos entre sus países
        for n in range(len(j.territorios) // 2):
            j.usar_reservas(1, rn.choice(j.territorios))

# Mostrar mapa final de la partida
dibujar(paises, coordenadas)
