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
    """Pieza de ajedrez genérica."""

    def __init__(self, color: str, símbolo: str, nombre: str) -> None:
        self.color: str = color
        self.simbolo: str = símbolo
        self.nombre: str = nombre

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """True si la pieza puede ir de origen a destino según sus reglas.""" 
        return False    #Cada subclase lo definirá

# ________ Subclases: tipos de pieza y definición de movimientos validos ________

class Torre(Pieza):
    """Se mueve en línea recta por filas o columnas."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea en línea recta y no haya piezas en el camino."""

        if origen[0] != destino[0] and origen[1] != destino[1]:     #Si cambian la fila y la columna al mismo tiempo, es un movimiento diagonal
            return False                                            #y no está permitido.
        
        #Llama al método camino_libre() del tablero: si este devuelve True, el movimiento de la torre también devuelve True. Si devuelve False, el movimiento devuelve False.
        return tablero.camino_libre(origen, destino)

class Caballo(Pieza):
    """Representa un caballo de ajedrez."""
    pass

class Alfil(Pieza):
    """Se mueve en diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Si recorre el mismo número de casillas por las filas y por las columnas y no hay piezas en el camino."""

        #Si la diferencia de filas y columnas no es la misma,  el movimiento no es diagonal y devuelve False.
        if abs(destino[0] - origen[0]) != abs(destino[1] - origen[1]):     #abs() compara las distancias sin importar la dirección hacia la que se mueve el alfil.
            return False
                
        #Llama al método camino_libre() del tablero: si este devuelve True, el movimiento de la torre también devuelve True. Si devuelve False, el movimiento devuelve False.
        return tablero.camino_libre(origen, destino)

class Dama(Pieza):
    """Representa una dama de ajedrez."""
    pass

class Rey(Pieza):
    """Representa un rey de ajedrez."""
    pass

class Peón(Pieza):
    """Representa un peón de ajedrez."""
    pass


# __________ Tablero __________

class Tablero:
    """Guarda la posición de las piezas y las operaciones sobre el tablero."""

    def __init__(self) -> None:

        #Construye una lista de listas que es una matriz de 8x8 vacía.
        self.casillas: list[list[Pieza | None]] = [
            [None for _ in range(TAMANO_TABLERO)]
            for _ in range(TAMANO_TABLERO)
        ]

        #Rellena la matriz con las piezas en sus posiciones iniciales.
        self.colocar_posicion_inicial()

# _____ Métodos _____

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
            self.casillas[1][columna] = Pieza("negra", "♟", "peón")

        #Peones blancos en séptima fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[6][columna] = Pieza("blanca", "♙", "peón")

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
        """Mueve una pieza desde la casilla de origen hasta la casilla de destino."""

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
    
        #La casilla de destino está ocupada por una pieza, esta es sustituida (*CAPTURA PROVISIONAL).
        self.casillas[fila_destino_tablero][columna_destino] = pieza
        self.casillas[fila_origen_tablero][columna_origen] = None   #Y se vacía la casilla de origen.

        return True

    def camino_libre(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Comprueba si las casillas situadas entre el origen y el destino están vacías."""

        diferencia_filas: int = destino[0] - origen[0]  #El valor de la diferencia indica el sentido en el que se recorren las filas.
        if diferencia_filas > 0:    
            paso_fila: int = 1        #Si es positiva, se avanza de una en una hacia arriba.
        elif diferencia_filas < 0:
            paso_fila: int = -1       #Si es negativa, se retrocede de una en una hacia abajo.
        else:
            paso_fila: int = 0        #Si es cero, las filas son las mismas (no se cambia de fila).

        diferencia_columnas: int = destino[1] - origen[1]   #El valor de la diferencia indica el sentido en el que se recorren las columnas.
        if diferencia_columnas > 0:       
            paso_columna: int = 1           #Si es positiva, se avanza de una en una hacia la derecha.
        elif diferencia_columnas < 0:       
            paso_columna: int = -1          #Si es negativa, se retrocede de una en una hacia izquierda.
        else:
            paso_columna: int = 0           #Si es cero, las columnas son las mismas (no se cambia de columna).

        #Comprobación del camino:

        #Se empieza por la primera casilla posterior al origen: se suma el paso correspondiente a las coordenadas iniciales.
        fila_actual: int = origen[0] + paso_fila
        columna_actual: int = origen[1] + paso_columna

        #Mientras no se llegue al destino, se repite la comprobación de condiciones siguiente:
        while (fila_actual, columna_actual) != destino:     #El destino no se comprueba porque puede haber una pieza rival a capturar."""

            fila_tablero: int = TAMANO_TABLERO - 1 - fila_actual    #Conversión de la fila al índice de la matriz (fila 8 arriba, fila 1 abajo).
            
            #Consulta de pieza en la casilla a comprobar: #Si hay una, termina el método. Si está vacía, avanza a la siguiente casilla.
            pieza: Pieza | None = self.casillas[fila_tablero][columna_actual]
            if pieza is not None:
                return False
            else:
                fila_actual = fila_actual + paso_fila           
                columna_actual = columna_actual + paso_columna

        return True     #El bucle Si se llega al destino sin encontrar obstáculos, el camino está libre.


# __________ Pruebas __________

#Tablero con posición inicial.
tablero = Tablero()
tablero.imprimir_tablero()

# __________ Prueba del alfil __________

#Crear un alfil blanco en c1 (fila 7, columna 2).
alfil_prueba: Alfil = Alfil("blanca", "♗", "alfil")
tablero.casillas[7][2] = alfil_prueba

#1: De c1 a f4 (! El peón de d2 bloquea el camino, devolverá False).
print(alfil_prueba.es_movimiento_valido(tablero, (0, 2), (3, 5)))

    #Se quita el peón:
tablero.casillas[6][3] = None

#2: Otra vez, pero sin el peón (Ahora devolverá True)
print(alfil_prueba.es_movimiento_valido(tablero, (0, 2), (3, 5)))

#3: De c1 a c4 (! Es movimiento vertical, devolverá False).
print(alfil_prueba.es_movimiento_valido(tablero, (0, 2), (3, 2)))