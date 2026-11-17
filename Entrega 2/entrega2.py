# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8     #El tablero de ajedrez tiene siempre 8 filas y 8 columnas.
LETRAS_VALIDAS: str = "abcdefgh"    #Las columnas del tablero se identifican con las letras de la 'a' a la 'h'.
NUMEROS_VALIDOS: str = "12345678"    #Las filas del tablero se identifican con los números de la '1' a la '8'.
CASILLA_VACIA: str = "·"    #Símbolo que representa una casilla vacía en el tablero.

#__________Clases__________

class Pieza:
    """Representa una pieza de ajedrez."""

    def __init__(self, color: str, simbolo: str, nombre: str) -> None:  #Inicializa una pieza con su color, símbolo y nombre.
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre

    def es_movimiento_valido(   #Comprueba si el movimiento de la pieza es válido. IMPLEMENTAR EN LAS SUBCLASES DE PIEZA
        self,
        tablero: "Tablero",
        origen: tuple[int, int],
        destino: tuple[int, int]
    ) -> bool:
        return False

class Tablero:
    """Representa el tablero de ajedrez."""

    #Creación del tablero y colocación de las piezas iniciales:

    def __init__(self) -> None:

        #Construye una lista de listas que es una matriz de 8x8 vacía.
        self.casillas: list[list[Pieza | None]] = [
            [None for _ in range(TAMANO_TABLERO)]
            for _ in range(TAMANO_TABLERO)
        ]

        #Rellena la matriz con las piezas en sus posiciones iniciales.
        self.colocar_piezas_iniciales()

    #Métodos:

    def colocar_piezas_iniciales(self) -> None:
        """Coloca todas las piezas en sus posiciones iniciales."""

        #Definimos las piezas: nombre y símbolo.

        piezas_blancas: list[tuple[str, str]] = [
            ("torre", "♖"),
            ("caballo", "♘"),
            ("alfil", "♗"),
            ("dama", "♕"),
            ("rey", "♔"),
            ("alfil", "♗"),
            ("caballo", "♘"),
            ("torre", "♖")
        ]

        piezas_negras: list[tuple[str, str]] = [
            ("torre", "♜"),
            ("caballo", "♞"),
            ("alfil", "♝"),
            ("dama", "♛"),
            ("rey", "♚"),
            ("alfil", "♝"),
            ("caballo", "♞"),
            ("torre", "♜")
        ]

        #Distribución de las piezas:

        #Piezas negras: primera fila
        for columna in range(TAMANO_TABLERO):
            nombre, símbolo = piezas_negras[columna]
            self.casillas[0][columna] = Pieza("negra", símbolo, nombre)
        
        #Peones negros: segunda fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[1][columna] = Pieza("negra", "♟", "peon")

        #Peones blancos: séptima fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[6][columna] = Pieza("blanca", "♙", "peon")

        #Piezas blancas: octava fila
        for columna in range(TAMANO_TABLERO):
            nombre, símbolo = piezas_blancas[columna]
            self.casillas[7][columna] = Pieza("blanca", símbolo, nombre)

    def imprimir_tablero(self) -> None:
        """Muestra el tablero con sus coordenadas."""

        print("  a b c d e f g h")

        for fila in range(TAMANO_TABLERO):
            print(8 - fila, end=" ")

            for columna in range(TAMANO_TABLERO):
                pieza = self.casillas[fila][columna]

                if pieza is None:
                    print("·", end=" ")
                else:
                    print(pieza.simbolo, end=" ")

            print()     ##Se muestra la línea completa con el símbolo de cada casilla.

#Prueba del tablero y las piezas

tablero = Tablero()
tablero.colocar_piezas_iniciales()
tablero.imprimir_tablero()