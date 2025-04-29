
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import json

# Carga el tablero
image = Image.open("data/teg.jpg")

# Carga las coordenadas de los países
with open("data/country_coordinates.json", "r", encoding="utf-8") as f:
    country_coordinates = json.load(f)

# Crea una figura
fig, ax = plt.subplots(figsize=(10, 8))

# Display the image
ax.imshow(image)

def dibuja_ejercitos_en_pais(country_name, number, color="red"):
    '''
    Dibuja un círculo de color `color` en el país `country_name` con el número `number` dentro.
    country_name: str
        Nombre del país donde se dibuja el círculo.
    number: int
        Número que se dibuja dentro del círculo, que representa el número de ejércitos.
    color: str
        Color del círculo. Por defecto es rojo.
    '''
    if country_name not in country_coordinates:
        print(f"Country '{country_name}' not found in coordinates.")
        return

    # Obtien las coordenadas del país
    x, y = country_coordinates[country_name]

   
    radius = 20
    # Dibuja el círculo
    circle = Circle((x, y), radius=radius, edgecolor='black', facecolor=color, linewidth=1, alpha=0.8)
    ax.add_patch(circle)

    # Agrega el número dentro del círculo
    ax.text(x, y, str(number), color="black", fontsize=12, ha="center", va="center")

    # Remueve los ejes
    ax.axis('off')


# Ejemplos de uso
dibuja_ejercitos_en_pais("Sahara", 5)
dibuja_ejercitos_en_pais("Zaire", 8, color="blue")
dibuja_ejercitos_en_pais("Madagascar", 4, color="green")



plt.show()

# Guarda la figura

fig.savefig("data/countries_with_armies.png", bbox_inches='tight', dpi=300)