import json
from pathlib import Path
import random as rn
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from modules.cartas import Mazo
from modules.jugador import Jugador
from modules.pais import Pais

# Funciones


def tiros(m: int, participantes):
    """Función a la que se le pasa una lista de objetos Jugador. Hace
    que todos estos jugadores lancen un dado y compara sus resultados.
    Indica quienes son los m jugadores con los mayores resultados. La
    función tiene en cuenta los empates"""

    ganadores = []
    jugs = participantes.copy()

    while True:

        # Todos los jugadores de la lista tiran dados

        for a in jugs:
            a.lanzar(1)

        # Los jugadores se ordenan según sus dados en orden descendente

        jugs.sort(key=lambda x: x.dado[0], reverse=True)
        valores = [i.dado[0] for i in jugs]

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


def dibujar(paises):
    """
    Dibuja un círculo de color `color` en el país `country_name` con el número `number` dentro.
    country_name: str
        Nombre del país donde se dibuja el círculo.
    number: int
        Número que se dibuja dentro del círculo, que representa el número de ejércitos.
    color: str
        Color del círculo. Por defecto es rojo.
    """

    # Crea una figura
    fig, ax = plt.subplots(figsize=(10, 8))

    # Muestra la imagen
    ax.imshow(Image.open("data/teg.jpg"))

    for a in paises:

        # Obtiene las coordenadas del país
        x, y = coordenadas[a.nombre]

        radio = 20
        # Dibuja el círculo
        circulo = Circle(
            (x, y),
            radius=radio,
            edgecolor="black",
            facecolor=a.jugador.color,
            linewidth=1,
            alpha=0.8,
        )
        ax.add_patch(circulo)

        # Agrega el número dentro del círculo
        ax.text(x, y, str(a.ejercitos), color="black", fontsize=12, ha="center", va="center")

        # Remueve los ejes
        ax.axis("off")


# Carga las coordenadas de los países
with open("data/country_coordinates.json", "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

## INICIALIZACIÓN

# Abrir las cartas. Se considera al 0 de la lista como el tope del mazo

with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
    cartas = json.load(f)

# Se crean los objetos Pais por cada país en el mazo de cartas. Luego se
# crea un objeto Mazo donde cada carta es un objeto pais

mazo1 = []
[mazo1.extend(i) for i in cartas.values()]
paises = [Pais(i) for i in mazo1]

mazo = Mazo(paises)
mazo.mezclar()

descarte = Mazo([])

# Crear jugadores

colores = ["cyan", "orange", "green", "red", "white", "pink"]

numJ = 4

J = [Jugador(f"José {i+1}", j) for i, j in enumerate(colores[:numJ])]

# Removí el atributo territorios de los jugadores. Consideré redundante
# que los objetos Pais tengan asociado on jugador y que a la vez los
# jugadores tengan una lista de países

# Repartir paí­ses por jugador. Recordar que pueden sobrar dos cartas si jugadores=3,4,6

if len(mazo) % numJ == 0:
    mano = len(mazo) // numJ
    [i.robar(mano, mazo) for i in J]
else:
    mano = (len(mazo) - 2) // numJ
    [i.robar(mano, mazo) for i in J]

    # Introducir el tiro de dados y las dos cartas extra

    [i.robar(1, mazo) for i in tiros(2, J)]

# Cada jugador añade 1 ejército a sus países. Los países de un jugador
# son objetos Pais

[i.reclamar(i.cartas, 1) for i in J]

# Quitar las cartas de las manos de los jugadores y resetear el mazo de cartas

# ¡ES PROBABLE QUE CAMBIE EL MÉTODO soltar SIMPLEMENTE POR LLAMAR A LAS
# CARTAS DEL JUGADOR!

[i.soltar(i.cartas, mazo) for i in J]

mazo.mezclar()

# Cada jugador añade 5 ejércitos repartidos entre sus paí­ses. Pueden
# reclamar la misma región más de una vez

[i.reclamos(5, [j for j in i.territorios]) for i in J]

# Cada jugador añade 3 ejércitos repartidos entre sus paí­ses

[i.reclamos(3, [j for j in i.territorios]) for i in J]

### TURNOS DE JUGADORES

## Reiniciando atributos de jugadores relevantes y atributos del mazo

# Reiniciar el atributo conquistador del Jugador, que volverá a ser
# obtenido si conquista un país esta ronda

[i.desconquistar() for i in J]

# Si el mazo se queda sin cartas, se usa las cartas descartadas
# para rellenar el mazo

if len(mazo) == 0:
    descarte.repartir(nombres=descarte, mazo=mazo)

mazo.mezclar()

# Determinar orden en el que juegan los jugadores

rn.shuffle(J)

dibujar(paises)
plt.show()

###TURNOS DE JUGADORES

victoria = False

for m in range(100):

    print("inicia ronda")
    print([i.territorios for i in J])
    # print([i.jugador for i in paises])

    for a in J:

        if len(a.territorios) <= 0:
            print(f"{a} ya no juega")
            continue

        # Quitar el atributo conquistador. Lo ganará si conquista un país

        a.desconquistar()
        a.futuro(None)

        ##FASE DE CANJE

        a.canjear(descarte)

        ##FASE DE ATAQUE

        # Falta implementar que el ataque sea opcional

        # El jugador revisa entre todos sus posibles países. Si pueden
        # atacar, estos revisan entre los limítrofes que pertenezcan a otro
        # país y entonces realizan el ataque. El jugador solo realiza un
        # ataque por turno

        # Quizás implementar sistema aleatorio de cuántos ataques realizar
        # y que ciertos países sean más probables que otros como atacantes

        # Quizás implemente que todos los chequeos de si un ataque es válido
        # en el método del jugador

        # Noté que en ataques aleatorios, los ejércitos tienden a
        # acumularse todos en unos pocos países. Esto evita que haya
        # expansión de territorios

        for n in range(rn.randint(2, 6)):
            # print('antes')
            # print([(i,i.ejercitos) for i in a.territorios])
            posibles = a.mis_paises()
            rn.shuffle(posibles)
            ofensiva = False
            for b in posibles:
                if b.ejercitos > 1 and not ofensiva:
                    lims = b.limitrofes.copy()
                    rn.shuffle(lims)
                    for c in lims:
                        d = [i for i in paises if i.nombre == c][0]
                        jug = d.jugador
                        # print([(i,i.ejercitos) for i in jug.territorios])
                        if d.jugador != a:
                            # print(f'pelean {b} y {d}')
                            a.atacar(b, d)
                            ofensiva = True
                            break

        if len(a.territorios) >= 40:
            victoria = True
            ganador = a

        """print('despues')
        print([(i,i.ejercitos) for i in a.territorios])
        print([(i,i.ejercitos) for i in jug.territorios])"""

        ##FASE DE REAGRUPAMIENTO

        posibles = [i for i in a.mis_paises() if i.ejercitos > 1]

        # Implementar que el jugador tiende a mover ejércitos hacia
        # limítrofes con otros jugadores. Su objetivo es que países
        # rodeados de compañeros con más de un ejército mueve los ejércitos
        # sobrantes hacia límites con otros jugadores

        # Quizás implemente todos los chequeos de si un movimiento es válido
        # en un método del jugador

        """print("antes de movimiento")
        print([(i, i.ejercitos) for i in a.territorios])"""

        if posibles:
            for b in range(rn.randint(0, 4)):
                movimiento = rn.choice(posibles)
                objetivo = [
                    i
                    for i in paises
                    if i.nombre in movimiento.limitrofes and i.jugador == a
                ]
                if not objetivo:
                    break
                elif movimiento.ejercitos > 2:
                    # elobjetivo=rn.choice(objetivo)
                    # print(f'hubo movimiento de {movimiento} a {elobjetivo}')

                    # Quizás use numpy acá porque no tiene problemas si el número
                    # de ejércitos es 2. Me ahorro un condicional
                    movimiento.mover(
                        rn.randint(1, movimiento.ejercitos - 1), rn.choice(objetivo)
                    )
                else:
                    # elobjetivo=rn.choice(objetivo)
                    # print(f'hubo movimiento de {movimiento} a {elobjetivo}')
                    movimiento.mover(1, rn.choice(objetivo))

        """print('despues de movimiento')
        print([(i,i.ejercitos) for i in a.territorios])"""

        # Crear una función que agrupe países del jugador en grupos según si
        # son limítrofes o no

        ##FASE DE LLAMADO

        # Chequear si jugador conquistó al menos un territorio para iniciar
        # esta fase

        if a.conquistador:
            a.robar(1, mazo)
            """print('antes')
            print([(i,i.ejercitos) for i in a.territorios])"""
            if a.cartas[-1] in a.territorios:
                a.reclamar([a.cartas[-1]], 2)
            else:
                a.futuro(a.cartas[-1])
            """print('despues')
            print([(i,i.ejercitos) for i in a.territorios])"""

        if len(mazo) == 0:
            descarte.repartir(n=len(descarte), mazo=mazo)

        ##FASE DE REFUERZO

        refuerzos = len(a.territorios) // 2

        for n in range(refuerzos):
            a.usar(1, rn.choice(a.territorios))


dibujar(paises)
plt.show()

"""print(ganador)
print([i.territorios for i in J])"""
