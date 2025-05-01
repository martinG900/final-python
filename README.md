# final-python
Simulación de una partida del juego de mesa TEG, jugado por jugadores simulados con decisiones tomadas de forma aleatoria.

Para la inicialización del juego, escribí un par de programas. 'data\chequeo_limites.py' y 'data\limites.py'. Sirvieron para crear un diccionario con los países limítrofes de cada país. El diccionario 'data\limites_preliminar.json' ayudó a este fin. El resultado de este tratamiento es 'data\limites.json', usado en main.py.

Una vez creado este diccionario, los programas mencionados ya no son útiles. Pueden ignorarse. Los dejé en la carpeta por si fueran necesarios en el futuro.

Las imágenes 'data\inicio.png' y 'data\ronda 1000.png' muestran ejemplos de la ejecución de main.py. Muestran el tablero al inicio del juego y tras mil rondas usando seis jugadores.

Si se quiere modificar el número de jugadores, cambiar 'numero_jugadores' en main.py. Es la única variable que es necesaria alterarse manualmente.

El módulo 'modules\muestra_ejercitos.py' se usó para confeccionar 'modules\dibujar.py', pero a parte de eso no forma parte del programa principal.