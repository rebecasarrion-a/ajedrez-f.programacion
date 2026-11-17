# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8     #El tablero de ajedrez tiene siempre 8 filas y 8 columnas.
LETRAS_VALIDAS: str = "abcdefgh"    #Las columnas del tablero se identifican con las letras de la 'a' a la 'h'.
NUMEROS_VALIDOS: str = "12345678"    #Las filas del tablero se identifican con los números de la '1' a la '8'.
CASILLA_VACIA: str = "·"    #Símbolo que representa una casilla vacía en el tablero.


# __________ Casilla: funciones __________

# ________ Representación de una casilla ________

def convertir_casilla_a_coordenadas(casilla: str) -> tuple[int, int]:
    """Convierte una casilla "letra número" en una tupla (fila, columna)."""

    fila: int = int(casilla[1]) - 1     #Convierte el "número" en un índice de fila. Se resta 1 para adaptar la numeración del ajedrez (1-8) a los índices internos (0-7).
    columna: int = LETRAS_VALIDAS.index(casilla[0])     #Buscando la "letra" en LETRAS_VALIDAS, index() devuelve su posición empezando desde 0, esa es la columna.

    return fila, columna    #Devuelve la coordenada (fila, columna).

# ________ Comprobación de una casilla ________

def es_casilla_valida(casilla: str) -> bool:
    """Comprueba si el texto recibido representa una casilla válida del tablero."""

    if len(casilla) != 2:   #Debe tener exactamente dos caracteres.
        return False

    if casilla[0] not in LETRAS_VALIDAS:    #El primero, una letra de LETRAS_VALIDAS.
        return False

    if casilla[1] not in NUMEROS_VALIDOS:   #El segundo, un número de NUMEROS_VALIDAS.
        return False

    return True     #Cuando supera todas las condiciones, es válida.

# ________ Formato de un movimiento ________

def procesar_movimiento(texto: str) -> tuple[str, str] | None:
    """Limpia y comprueba la validez del formato de un movimiento introducido."""

    movimiento: str = texto.strip().lower()     #Con el texto introducido: se eliminan espacios sobrantes (strip) y se convierte a minúsculas (lower).
    partes: list[str] = movimiento.split()      #Separamos el texto origen y el texto destino con espacios (strip).

    #Un movimiento debe contener exactamente dos casillas.
    if len(partes) != 2:    
        return None         #Si no es así, devuelve None.

    #Se guardan los dos en variables independientes y se comprueba que sean casillas válidas.
    origen: str = partes[0]
    destino: str = partes[1]

    if not es_casilla_valida(origen) or not es_casilla_valida(destino):
        return None     #Si no es así, devuelve None.

    return origen, destino  #DCuando supera todas las condiciones, devuelve el movimiento en el formato correcto.


# __________ Pieza: clase, método y subclases __________

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

#De moment en les sublases pose pass perq no tenim moviments
class Torre(Pieza):
    """Representa una torre de ajedrez."""
    pass

class Caballo(Pieza):
    """Representa un caballo de ajedrez."""
    pass

class Alfil(Pieza):
    """Representa un alfil de ajedrez."""
    pass

class Dama(Pieza):
    """Representa una dama de ajedrez."""
    pass

class Rey(Pieza):
    """Representa un rey de ajedrez."""
    pass

class Peon(Pieza):
    """Representa un peón de ajedrez."""
    pass


# __________ Tablero: clase y métodos __________ *AÑADIR ANOTACIONES Y EXPLICACIONES

class Tablero:
    """Representa el tablero de ajedrez."""

    def __init__(self) -> None:

        #Construye una lista de listas que es una matriz de 8x8 vacía.
        self.casillas: list[list[Pieza | None]] = [
            [None for _ in range(TAMANO_TABLERO)]
            for _ in range(TAMANO_TABLERO)
        ]

        #Rellena la matriz con las piezas en sus posiciones iniciales.
        self.colocar_posicion_inicial()

# _____ Métodos: colocar de piezas, imprimir tablero y mover pieza _____

    def colocar_posicion_inicial(self) -> None:
        """Coloca todas las piezas en sus posiciones iniciales."""

        #Definición de piezas (nombre y símbolo) y su distribución.

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

        #Piezas negras en primera fila
        for columna in range(TAMANO_TABLERO):
            nombre, símbolo = piezas_negras[columna]
            self.casillas[0][columna] = Pieza("negra", símbolo, nombre)
        
        #Peones negros en segunda fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[1][columna] = Pieza("negra", "♟", "peon")

        #Peones blancos en séptima fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[6][columna] = Pieza("blanca", "♙", "peon")

        #Piezas blancas en octava fila
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

    def mover_pieza(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Mueve una pieza desde la casilla de origen hasta la casilla de destino. SIN REGLAS."""

        #Se separa la fila y la columna de las casillas de origen y destino.
        fila_origen: int = origen[0]
        columna_origen: int = origen[1]

        fila_destino: int = destino[0]
        columna_destino: int = destino[1]

        #Conversión de filas a los índices utilizados por la matriz (fila 8 arriba, fila 1 abajo).
        fila_origen_tablero: int = TAMANO_TABLERO - 1 - fila_origen
        fila_destino_tablero: int = TAMANO_TABLERO - 1 - fila_destino

    #El movimiento no se realiza (return False) cuando:
        
        #El origen y el destino son los mismos.
        if origen == destino:
            return False

        #La casilla de origen está vacía.
        pieza: Pieza | None = self.casillas[fila_origen_tablero][columna_origen]    #Comprobación.

        if pieza is None:
            return False

    #El movimiento se realiza correctamente (return True), si:
    
        #La casilla de destino está ocupada por una pieza, esta es sustituida (CAPTURA PROVISIONAL).
        self.casillas[fila_destino_tablero][columna_destino] = pieza
        self.casillas[fila_origen_tablero][columna_origen] = None   #Y se vacía la casilla de origen.

        return True

# __________ Pruebas de este commit __________

#Crea un tablero con posición inicial.
tablero = Tablero()

#Movimiento: peón blanco de e2 a e4.
movimiento_realizado: bool = tablero.mover_pieza((1, 4), (3, 4))

#¿Se ha realizado correctamente? Imprimir movimiento.
tablero.imprimir_tablero()