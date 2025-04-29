from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Circle


def dibujar(paises: list, coordenadas: dict):
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
        ax.text(
            x, y, str(a.ejercitos), color="black", fontsize=12, ha="center", va="center"
        )

        # Remueve los ejes
        ax.axis("off")

    plt.show()
