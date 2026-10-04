# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"

# __________ Estructuras de datos: posición inicial __________

tablero_simbolos: list[list[str]] = [
    ["\u265C", "\u265E", "\u265D", "\u265B", "\u265A", "\u265D", "\u265E", "\u265C"],
    ["\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659"],
    ["\u2656", "\u2658", "\u2657", "\u2655", "\u2654", "\u2657", "\u2658", "\u2656"]
]

tablero_nombres: list[list[str]] = [
    ["torre negra", "caballo negro", "alfil negro", "reina negra",
     "rey negro", "alfil negro", "caballo negro", "torre negra"],
    ["peón negro", "peón negro", "peón negro", "peón negro", "peón negro", "peón negro", "peón negro", "peón negro"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"], 
    ["·", "·", "·", "·", "·", "·", "·", "·"], 
    ["·", "·", "·", "·", "·", "·", "·", "·"], 
    ["peón blanco", "peón blanco", "peón blanco", "peón blanco", "peón blanco", "peón blanco", "peón blanco", "peón blanco"],
    ["torre blanca", "caballo blanco", "alfil blanco", "reina blanca",
     "rey blanco", "alfil blanco", "caballo blanco", "torre blanca"]
]

# __________ Impresión del tablero __________

encabezado: str = "  "

for indice_columna in range(TAMANO_TABLERO):
    letra_columna: str = LETRAS_VALIDAS[indice_columna]
    encabezado: str = encabezado + " " + letra_columna + " "
print(encabezado)

for indice_fila in range(TAMANO_TABLERO):
    numero_fila: int = TAMANO_TABLERO - indice_fila
    linea: str = str(numero_fila) + " "
    for indice_columna in range(TAMANO_TABLERO):
        simbolo: str = tablero_simbolos[indice_fila][indice_columna]
        if simbolo == "·":
            celda: str = " · "
        else:
            celda: str = " " + simbolo + " "
        linea: str = linea + celda
    print(linea)


print("")
print("Escribe una casilla o 'salir' para terminar el juego.")
print("")

# __________ Bucle principal: máquina de estados __________

estado: str = "turno_blancas" # SIEMPRE empieza así

while estado != "salir":
    
    if estado == "turno_blancas":
        print("Turno de las blancas")
        casilla: str = input("Casilla a consultar: ")

        if casilla == "salir":
            estado = "salir"

        elif len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS:
            letra_columna: str = casilla[0]
            columna: int = 0
    
            if letra_columna == "a":
                columna = 0
            elif letra_columna == "b":
                columna = 1
            elif letra_columna == "c":
                columna = 2
            elif letra_columna == "d":
                columna = 3
            elif letra_columna == "e":
                columna = 4
            elif letra_columna == "f":
                columna = 5
            elif letra_columna == "g":
                columna = 6
            elif letra_columna == "h":
                columna = 7

            fila_tablero: int = TAMANO_TABLERO - int(casilla[1])
            nombre_pieza: str = tablero_nombres[fila_tablero][columna]

            if nombre_pieza == "·":
                print(f"La casilla {casilla} está vacía.")
            else:
                print(f"En {casilla} se encuentra: {nombre_pieza}.")

            estado = "turno_negras"
    
        else:
            print("Casilla no válida.")

    elif estado == "turno_negras":
        print("Turno de las negras")
        casilla = input("Casilla a consultar: ")

        if casilla == "salir":
            estado = "salir"

        elif len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS:
            letra_columna = casilla[0]
            columna = 0

            if letra_columna == "a":
                columna = 0
            elif letra_columna == "b":
                columna = 1
            elif letra_columna == "c":
                columna = 2
            elif letra_columna == "d":
                columna = 3
            elif letra_columna == "e":
                columna = 4
            elif letra_columna == "f":
                columna = 5
            elif letra_columna == "g":
                columna = 6
            elif letra_columna == "h":
                columna = 7

            fila_tablero = TAMANO_TABLERO - int(casilla[1])
            nombre_pieza = tablero_nombres[fila_tablero][columna]

            if nombre_pieza == "·":
                print(f"La casilla {casilla} está vacía.")
            else:
                print(f"En {casilla} se encuentra: {nombre_pieza}.")

            estado = "turno_blancas"

        else:
            print("Casilla no válida.")