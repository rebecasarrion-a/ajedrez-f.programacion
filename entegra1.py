# __________ Constantes del tablero __________
 
TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = " abcdefgh"
NUMEROS_VALIDOS: str = "12345678"

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

for letras in LETRAS_VALIDAS:
    print(letras, end=" ")
print()

for fila in tablero_simbolos:
    for pieza in fila:
        print(pieza, end=" ")
    print()

#PARA cada fila del tablero:
    #PARA cada casilla de esa fila:
        #imprimir la casilla

