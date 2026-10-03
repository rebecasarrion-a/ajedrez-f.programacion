# __________ Constantes del tablero __________
 
TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"

# __________ Estructuras de datos: posición inicial __________

tablero_simbolos: list[list[str]] = [
    ["\u265C", "\u265E", "\u265D", "\u265B", "\u265A", "\u265D", "\u265E", "\u265C"],
    ["\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", ".", "."], 
    ["\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659"],
    ["\u2656", "\u2658", "\u2657", "\u2655", "\u2654", "\u2657", "\u2658", "\u2656"]
]

tablero_nombres: list[list[str]] = [
    ["torre negra", "caballo negro", "alfil negro", "reina negra",
     "rey negro", "alfil negro", "caballo negro", "torre negra"],
    ["peon negro", "peon negro", "peon negro", "peon negro", "peon negro", "peon negro", "peon negro", "peon negro"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", ".", "."], 
    ["peon blanco", "peon blanco", "peon blanco", "peon blanco", "peon blanco", "peon blanco", "peon blanco", "peon blanco"],
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
    numero_fila: int = TAMANO_TABLERO -indice_fila
    linea: str = str(numero_fila) + " "
    for indice_columna in range(TAMANO_TABLERO):
        simbolo: str = tablero_simbolos[indice_fila][indice_columna]
        if simbolo == "":
            celda: str = " . "
        else:
            celda: str = " " + simbolo + " "
        linea: str = linea + celda
    print(linea)

print("")
print("Escribe una casilla o 'salir' para terminar el juego.")
print("")