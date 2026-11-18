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

    return fila, columna    #Devuelve una coordenada (fila, columna).

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
    partes: list[str] = movimiento.split()      #Separamos el texto origen y el texto destino con espacios (split).

    #Un movimiento debe contener exactamente dos casillas.
    if len(partes) != 2:    
        return None         #Si no es así, devuelve None.

    #Se guardan los dos en variables independientes y se comprueba que sean casillas válidas.
    origen: str = partes[0]
    destino: str = partes[1]

    if not es_casilla_valida(origen) or not es_casilla_valida(destino):
        return None

    return origen, destino  #Cuando supera todas las condiciones, devuelve el movimiento en el formato correcto.


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
        
        return tablero.camino_libre(origen, destino)    #Si se mueve en línea recta, devuelve lo que devuelva el método camino_libre().

class Caballo(Pieza):
    """Se mueve en forma de L y puede saltar por encima de otras piezas."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento tenga forma de L."""

        diferencia_filas: int = abs(destino[0] - origen[0])
        diferencia_columnas: int = abs(destino[1] - origen[1])

        if not ((diferencia_filas == 2 and diferencia_columnas == 1) or
                (diferencia_filas == 1 and diferencia_columnas == 2)):
            return False
        
        return True

class Alfil(Pieza):
    """Se mueve en diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea en diagonal y no hay piezas en el camino."""

        #Si la diferencia de filas no coincide con la decolumnas no es la misma, el movimiento no es diagonal y devuelve False.
        if abs(destino[0] - origen[0]) != abs(destino[1] - origen[1]):     #abs() compara las distancias sin importar la dirección hacia la que se mueve el alfil.
            return False
                
        return tablero.camino_libre(origen, destino)    #Si es la misma, devuelve lo que devuelva el método camino_libre().

class Dama(Pieza):
    """Se mueve en horizontal, vertical o diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea horizontal, vertical o diagonal y no haya piezas en el camino."""

        #Definición de los movimientos permitidos:
        movimiento_recto: bool = (origen[0] == destino[0] or origen[1] == destino[1])
        movimiento_diagonal: bool = (abs(destino[0] - origen[0]) == abs(destino[1] - origen[1]))

        if not movimiento_recto and not movimiento_diagonal:
            return False

        return tablero.camino_libre(origen, destino)    #Si se cumplen, devuelve lo que devuelva el método camino_libre().

class Rey(Pieza):
    """Se mueve una casilla, en cualquier dirección."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que se desplace una sola casilla."""

        if abs(destino[0] - origen[0]) > 1 or abs(destino[1] - origen[1]) > 1:
            return False
        else:
            return True     #Si las distancias son 1, el movimiento es válido.

class Peón(Pieza):

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Se mueve una casilla, o dos si es el primer movimiento.
        También puede capturar una pieza rival desplazándose una casilla en diagonal hacia delante."""

        #Dirección de avance según color.
        if self.color == "blanca":  #Blancas avanzan aumentando la fila.
            direccion: int = 1
            fila_inicial: int = 1
        else:                       #Negras avanzan disminuyéndola.
            direccion = -1
            fila_inicial = 6

        #Calculo de la distancia que se desplaza el peón por filas y columnas.
        diferencia_filas: int = destino[0] - origen[0]
        diferencia_columnas: int = abs(destino[1] - origen[1])

        fila_destino_tablero: int = TAMANO_TABLERO - 1 - destino[0]     #Conversión de la fila al índice de la matriz (fila 8 arriba, fila 1 abajo).

        #Consulta de pieza en la casilla de destino.
        pieza_destino: Pieza | None = tablero.casillas[fila_destino_tablero][destino[1]]

        # __ CASO GENERAL: avanzar una casilla hacia delante (el destino tiene que estar vacío) __
        
        if diferencia_filas == direccion and diferencia_columnas == 0:
            if pieza_destino is None:
                return True
            else:
                return False

        # __ CASO PRIMER MOVIMIENTO: avanzar dos casillas hacia delante (el destino tiene que estar vacío) __
        
        if diferencia_filas == 2 * direccion and diferencia_columnas == 0:
            if origen[0] != fila_inicial:   #Solo puede hacerlo si todavía está en su fila inicial.
                return False

            # _ Casilla intermedia: posición y consulta _
            fila_intermedia: int = origen[0] + direccion
            fila_intermedia_tablero: int = TAMANO_TABLERO - 1 - fila_intermedia

            pieza_intermedia: Pieza | None = tablero.casillas[fila_intermedia_tablero][origen[1]]

            if pieza_intermedia is None and pieza_destino is None:      #Las dos casillas deben estar vacías para avanzar.
                return True
            else:
                return False

        # __ CASO CAPTURA: solo puede capturar al rival en diagonal __
        
        if diferencia_filas == direccion and diferencia_columnas == 1:      #Movimiento diagonal (avanza una fila y se desplaza una columna).
            if pieza_destino is not None:
                if pieza_destino.color != self.color:   #Solo captura si hay una pieza de otro color en el destino.
                    return True
            else:
                return False

        # Si no se cumple ninguno de los tres casos anteriores, el movimiento no está permitido para el peón.
        return False


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

        #Conversión de filas a los índices de la matriz.
        fila_origen_tablero: int = TAMANO_TABLERO - 1 - fila_origen
        fila_destino_tablero: int = TAMANO_TABLERO - 1 - fila_destino

    #El movimiento no se realiza cuando:
        
        if origen == destino:       #El origen y el destino son los mismos.
            return False

        pieza: Pieza | None = self.casillas[fila_origen_tablero][columna_origen]
        if pieza is None:                                                           #La casilla de origen está vacía.
            return False

    #El movimiento se realiza correctamente (return True), si:
    
        #La casilla de destino está ocupada por una pieza, esta es sustituida (*CAPTURA PROVISIONAL).
        self.casillas[fila_destino_tablero][columna_destino] = pieza
        self.casillas[fila_origen_tablero][columna_origen] = None   #Y se vacía la casilla de origen.

        return True

    def camino_libre(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Comprueba si las casillas situadas entre el origen y el destino están vacías."""

        #El valor de las diferencias entre filas indica el sentido del desplazamiento por ellas.
        diferencia_filas: int = destino[0] - origen[0]
        if diferencia_filas > 0:    
            paso_fila: int = 1        #Se avanza de fila en fila hacia arriba.
        elif diferencia_filas < 0:
            paso_fila: int = -1       #Se retrocede de fila en fila hacia abajo.
        else:
            paso_fila: int = 0        #No se cambia de fila.

        #El valor de las diferencias entre columnas indica el sentido del desplazamiento por ellas.
        diferencia_columnas: int = destino[1] - origen[1]
        if diferencia_columnas > 0:       
            paso_columna: int = 1           #Se avanza de columna en columna hacia la derecha.
        elif diferencia_columnas < 0:       
            paso_columna: int = -1          #Se retrocede de columna en columna hacia izquierda.
        else:
            paso_columna: int = 0           #No se cambia de columna.

        #La comprobación empieza en la primera casilla posterior al origen.
        fila_actual: int = origen[0] + paso_fila
        columna_actual: int = origen[1] + paso_columna

        #Se recorren las casillas intermedias en un bucle while, sin comprobar el destino (puede haber un rival a capturar).
        while (fila_actual, columna_actual) != destino:

            fila_tablero: int = TAMANO_TABLERO - 1 - fila_actual    #Conversión de la fila al índice de la matriz.
            
            #Consulta de pieza en la casilla a comprobar:
            pieza: Pieza | None = self.casillas[fila_tablero][columna_actual]
            if pieza is not None:
                return False             #Si hay una, termina el método.

            #Si está vacía, avanza a la siguiente.
            fila_actual = fila_actual + paso_fila           
            columna_actual = columna_actual + paso_columna

        return True     #El método devuelve True si no han habido piezas en el camino.


# __________ Pruebas __________

#Tablero con posición inicial.
tablero = Tablero()
tablero.imprimir_tablero()