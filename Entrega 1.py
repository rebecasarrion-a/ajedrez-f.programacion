# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8     #El tablero de ajedrez tiene siempre 8 filas y 8 columnas.
LETRAS_VALIDAS: str = "abcdefgh"    #Las columnas del tablero se identifican con las letras de la 'a' a la 'h'.
NUMEROS_VALIDOS: str = "12345678"    #Las filas del tablero se identifican con los números de la '1' a la '8'.

# __________ Estructuras de datos: posición inicial __________

'Esta lista de listas representa visualmente el tablero con la posición inicial de las piezas en él.'
'Cada lista interior representa una fila y cada elemento en ella representa una casilla.'
'Los elementos contienen el símbolo correspondiente a cada casilla: pieza en símbolo Unicode o vacío "·".'

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

'Esta segunda lista de listas almacena el nombre de la pieza correspondiente a cada casilla.'
'Tiene exactamente la misma estructura que tablero_simbolos, de manera que una misma posición [fila][columna] corresponde a la misma casilla en ambas listas.'

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

'Se inicializa una cadena de texto que contendrá las letras correspondientes a las columnas del tablero.'

encabezado: str = "  "  #El encabezado incluye dos espacios para dejar espacio a los números de las filas.

for indice_columna in range(TAMANO_TABLERO):    #Se recorren las posiciones de las columnas mediante un bucle.
    letra_columna: str = LETRAS_VALIDAS[indice_columna]     #Para cada posición se obtiene la letra correspondiente de LETRAS_VALIDAS (0 > a, 1 > b...)
    encabezado: str = encabezado + " " + letra_columna + " "    #Se incorpora al encabezado con espacios alrededor para que quede centrada
    print(encabezado)   #Se muestra el encabezado con las letras de las columnas.

for indice_fila in range(TAMANO_TABLERO):   #Se recorren las posiciones de las filas mediante un bucle.
    numero_fila: int = TAMANO_TABLERO - indice_fila   #Como Las filas están ordenadas de arriba hacia abajo, restamos el índice al tamaño del tablero.
    linea: str = str(numero_fila) + " "     #La línea comienza colocando el número de la fila y le sigue un espacio para separar el número de las casillas.
    for indice_columna in range(TAMANO_TABLERO):    #Se recorren las posiciones de las columnas mediante un bucle.
        simbolo: str = tablero_simbolos[indice_fila][indice_columna]    #Obtenemos el símbolo que hay en la casilla actual:
        if simbolo == "·":
            celda: str = " · "
        else:
            celda: str = " " + simbolo + " "
        linea: str = linea + celda    #Se incorpora la casilla a la línea.
    print(linea)    #Se muestra la línea completa con el símbolo de cada casilla.

'Indicamos al usuario qué debe introducir, añadiéndo una línea en blanco antes y después por estética y claridad.'

print("")
print("Escribe una casilla o 'salir' para terminar el juego.")
print("")

# __________ Bucle principal: máquina de estados __________

'El juego utiliza una máquina de estados que alterna entre el turno de las blancas y el turno de las negras.'

    # ________ Turno de las blancas ________
    
# El estado inicial siempre es "turno_blancas".
estado: str = "turno_blancas"

'Mientras el estado no sea "salir", se repite el bucle principal.'

while estado != "salir":

    'Si el estado es "turno_blancas", se solicita al usuario una casilla para consultar.'

    if estado == "turno_blancas":
        print("Turno de las blancas")
        casilla: str = input("Casilla a consultar: ")

        'Si la respuesta es "salir", se cambia el estado a "salir" y el bucle termina.'

        if casilla == "salir":
            estado = "salir"    

            'Si la respuesta es otra, se comprueba que tiene el formato correcto: '
            ' - Dos caracteres, el primero una letra valida (LETRAS_VALIDAS) y el segundo un número válido (NUMEROS_VALIDOS).'

        elif len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS:
            letra_columna: str = casilla[0]     #Se obtiene la letra de la columna de la casilla introducida.   
            columna: int = 0   #Se inicializa la variable columna a 0, que se actualizará según la letra de la columna.

            #La letra de la columna se convierte en un índice de columna (0 a 7).
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
            #El número de la fila se convierte en un índice de fila (0 a 7) restando el número de la casilla al tamaño del tablero.
            fila_tablero: int = TAMANO_TABLERO - int(casilla[1])

            'El nombre de la pieza se obtiene utilizando fila y columna.'

            nombre_pieza: str = tablero_nombres[fila_tablero][columna]

            'Si la respuesta es "·", la casilla está vacía. Si no, se muestra el nombre de la pieza que hay en la casilla.'

            if nombre_pieza == "·":
                print(f"La casilla {casilla} está vacía.")
            else:
                print(f"En {casilla} se encuentra: {nombre_pieza}.")

            'Después de validar la casilla, se cambia el estado a "turno_negras".'

            estado = "turno_negras"

            'Si la entrada NO cumple el formato, se muestra el siguiente mensaje.'
            'El estado NO cambia: permanece en el mismo turno para poder intentarlo de nuevo.'
    
        else:
            print("Casilla no válida.")

    # ________ Turno de las negras ________

        'Este bloque funciona como el anterior, y después de una consulta válida devuelve el turno a las blancas.'

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

            'Si la casilla consultada es válida, el estado cambia a "turno_blancas".'

            estado = "turno_blancas"

            'Si la entrada NO cumple el formato, se muestra el siguiente mensaje.'
            'El estado NO cambia: permanece en el mismo turno para poder intentarlo de nuevo.'

        else:
            print("Casilla no válida.")