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

# Crear objeto Mazo cuyas cartas son objetos Pais
mazo = Mazo(paises)
mazo.mezclar()

# Crear Mazo de descarte
descarte = Mazo([])

numero_jugadores = 4

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

# Jugadores adquieren países y coloocan un ejército en cada uno
[i.desplegar(i.cartas, 1) for i in jugadores]
# Jugadores devuelven sus cartas al mazo
[i.soltar(i.cartas, mazo) for i in jugadores]

mazo.mezclar()

# Jugadores despliegan ejércitos en sus países
[i.despliegues(5, [j for j in i.territorios]) for i in jugadores]
[i.despliegues(3, [j for j in i.territorios]) for i in jugadores]

# Orden en el que juegan jugadores
rn.shuffle(jugadores)

# Estado inicial del mapa
dibujar(paises, coordenadas)


### BUCLE DE JUEGO

victoria = False

for m in range(100):  # O sino "while not victoria:"

    # Flujo para cada jugador
    for j in jugadores:
        # Revisar si jugador perdió y saltearlo
        if len(j.territorios) <= 0:
            continue

        ##FASE DE CANJE

        j.canjear(descarte)

        ##FASE DE ATAQUE

        # Realizar ataques un número aleatorio de veces
        for n in range(rn.randint(2, 6)):
            paises_atacantes = j.mis_paises()
            rn.shuffle(paises_atacantes)
            # Valor que revisa si se ganó un ataque, en cuyo caso
            # reinicia el bucle
            ataque_realizado = False
            for atacante in paises_atacantes:
                # Revisa si ataque es posible
                if atacante.ejercitos > 1 and not ataque_realizado:
                    # Define a los posibles objetivos del ataque
                    paises_limitrofes = atacante.limitrofes.copy()
                    rn.shuffle(paises_limitrofes)
                    for limitrofe in paises_limitrofes:
                        defensor = [i for i in paises if i.nombre == limitrofe][0]
                        # Revisa si el país elegido es de otro jugador
                        if defensor.jugador != j:
                            j.atacar(atacante, defensor)
                            ataque_realizado = True
                            break

        # Terminada la fase de ataque, el juguador pierde el país que
        # tenía como objetivo conquistar, dado por la carta robada en
        # la fase de Llamado
        j.objetivo(None)

        # Revisa condición de victoria
        if len(j.territorios) >= 40:
            victoria = True
            ganador = j

        ##FASE DE REAGRUPAMIENTO

        # Elegir posibles países que pueden desplegar tropas
        paises_movimiento = [i for i in j.mis_paises() if i.ejercitos > 1]

        if paises_movimiento:
            # Bucle de cuántos movimientos hará el jugador
            for m in range(rn.randint(2, 5)):
                pais_origen = rn.choice(paises_movimiento)
                # Solo movimientos a países propios
                paises_destino = [
                    i
                    for i in paises
                    if i.nombre in pais_origen.limitrofes and i.jugador == j
                ]
                if not paises_destino:
                    break
                else:
                    # Jugador mueve un número aleatorio de tropas
                    pais_origen.mover(
                        rn.randint(0, pais_origen.ejercitos - 1),
                        rn.choice(paises_destino),
                    )

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
                j.desplegar([j.cartas[-1]], 2)
            else:
                j.objetivo(j.cartas[-1])

        # Si cartas del mazo se acaban, usar el descarte para rellenarlo
        if len(mazo) == 0:
            descarte.repartir(n=len(descarte), mazo=mazo)

        ##FASE DE REFUERZO

        refuerzos = len(j.territorios) // 2

        # Jugador distribuye refuerzos entre sus países
        for n in range(refuerzos):
            j.usar_reservas(1, rn.choice(j.territorios))

# Mostrar mapa final de la partida
dibujar(paises, coordenadas)
