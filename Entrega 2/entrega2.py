# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8     #El tablero de ajedrez tiene siempre 8 filas y 8 columnas.
LETRAS_VALIDAS: str = "abcdefgh"    #Las columnas del tablero se identifican con las letras de la 'a' a la 'h'.
NUMEROS_VALIDOS: str = "12345678"    #Las filas del tablero se identifican con los números de la '1' a la '8'.
CASILLA_VACIA: str = "·"    #Símbolo que representa una casilla vacía en el tablero.

#__________Clases__________

    #__Clase pieza__

'Pieza de ajedrez genérica.'
class Pieza:

    def __init__(self, color: str, simbolo: str, nombre: str) -> None:  #Inicializa una pieza con su color, símbolo y nombre.
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre

    def es_movimiento_valido(   #Comprueba si el movimiento de la pieza es válido: será implementado en las subclases de Pieza.
        self,
        tablero: "Tablero",
        origen: tuple[int, int],
        destino: tuple[int, int]
    ) -> bool:
        return False

    #__Clase tablero__

'Guarda las piezas y las operaciones sobre el tablero.'
class Tablero:

    def __init__(self) -> None:   #Crea el tablero y coloca las piezas iniciales.
        self.casillas: list[list[Pieza | None]] = []
        self.colocar_posicion_inicial()

    def colocar_posicion_inicial(self) -> None:   #Rellena el tablero con la posición inicial estándar.
        pass

        #_Piezas blancas_

        piezas_blancas: list[tuple[str, str]] = [
            ("torre", "♖"),
            ("caballo", "♘"),
            ("alfil", "♗"),
            ("reina", "♕"),
            ("rey", "♔"),
            ("alfil", "♗"),
            ("caballo", "♘"),
            ("torre", "♖")
        ]

        #_Piezas negras_

        piezas_negras: list[tuple[str, str]] = [
            ("torre", "♜"),
            ("caballo", "♞"),
            ("alfil", "♝"),
            ("reina", "♛"),
            ("rey", "♚"),
            ("alfil", "♝"),
            ("caballo", "♞"),
            ("torre", "♜")
        ]

#FOR IN PARA COLOCAR LAS PIEZAS EN LA POSICIÓN INICIAL EN EL TABLERO