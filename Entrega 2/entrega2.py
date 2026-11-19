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
            if pieza_destino is not None and pieza_destino.color != self.color:   #Solo captura si hay una pieza de otro color en el destino.
                return True
            else:
                return False

        #Si no se cumple ninguno de los tres casos anteriores, el movimiento no está permitido para el peón.
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

        #Piezas negras en primera fila.
        for columna in range(TAMANO_TABLERO):
            nombre, simbolo = piezas_negras[columna]

            if nombre == "torre":
                self.casillas[0][columna] = Torre("negra", simbolo, nombre)
            elif nombre == "caballo":
                self.casillas[0][columna] = Caballo("negra", simbolo, nombre)
            elif nombre == "alfil":
                self.casillas[0][columna] = Alfil("negra", simbolo, nombre)
            elif nombre == "dama":
                self.casillas[0][columna] = Dama("negra", simbolo, nombre)
            elif nombre == "rey":
                self.casillas[0][columna] = Rey("negra", simbolo, nombre)
        
        #Peones negros en segunda fila.
        for columna in range(TAMANO_TABLERO):
            self.casillas[1][columna] = Peón("negra", "♟", "peón")

        #Peones blancos en séptima fila
        for columna in range(TAMANO_TABLERO):
            self.casillas[6][columna] = Peón("blanca", "♙", "peón")

        #Piezas blancas en octava fila
        for columna in range(TAMANO_TABLERO):
            nombre, simbolo = piezas_blancas[columna]

            if nombre == "torre":
                self.casillas[7][columna] = Torre("blanca", simbolo, nombre)
            elif nombre == "caballo":
                self.casillas[7][columna] = Caballo("blanca", simbolo, nombre)
            elif nombre == "alfil":
                self.casillas[7][columna] = Alfil("blanca", simbolo, nombre)
            elif nombre == "dama":
                self.casillas[7][columna] = Dama("blanca", simbolo, nombre)
            elif nombre == "rey":
                self.casillas[7][columna] = Rey("blanca", simbolo, nombre)


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

        print()  # Línea en blanco después del tablero.


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

            # ____ Validación general de movimientos ____


    def validar_movimiento(self, texto: str, color_turno: str) -> str:
        """Comprueba si un movimiento es válido para el jugador al que le corresponde el turno y explica el primer motivo de rechazo."""

        #1. Comprobación del formato con procesar_movimiento:
        movimiento: tuple[str, str] | None = procesar_movimiento(texto)

        if movimiento is None:
            return "Formato de movimiento no válido. Escribe origen y destino, por ejemplo: e2 e4."

            #Separamos las dos casillas que devuelve procesar_movimiento().
        casilla_origen: str = movimiento[0]
        casilla_destino: str = movimiento[1]
            #Convertimos ambas casillas a coordenadas (fila, columna).
        origen: tuple[int, int] = convertir_casilla_a_coordenadas(casilla_origen)
        destino: tuple[int, int] = convertir_casilla_a_coordenadas(casilla_destino)

        #2. Comprobación de origen y destino iguales:

        if origen == destino:
            return "Movimiento no válido. La pieza no se mueve."

        #3. Comprobación de que hay una pieza en el origen:

        fila_origen_tablero: int = TAMANO_TABLERO - 1 - origen[0]   #Conversión de la fila al índice de la matriz.

        pieza_origen: Pieza | None = self.casillas[fila_origen_tablero][origen[1]]

        if pieza_origen is None:
            return "Movimiento no válido. No hay ninguna pieza en la casilla de origen."

        #4. Comprobación del color del turno:

        if pieza_origen.color != color_turno:                                           #Solo se permite mover piezas del jugador al que le toca jugar.
            return "Movimiento no válido. Es el turno de las " + color_turno + "s."

        #5. Comprobación de pieza en el destino: diferente color y rey.

        fila_destino_tablero: int = TAMANO_TABLERO - 1 - destino[0]     #Conversión de la fila al índice de la matriz.

        pieza_destino: Pieza | None = self.casillas[fila_destino_tablero][destino[1]]       #Consulta si hay una pieza en el destino.

        if pieza_destino is not None:                        #Si la hay, no puede ser del mismo color de las piezas en turno.
            if pieza_destino.color == color_turno:
                return "Movimiento no válido. La casilla de destino está ocupada por una pieza propia."

        #El rey no se puede captura: la partida termina por jaque mate.
        if pieza_destino is not None:
            if pieza_destino.nombre == "rey":
                return "Movimiento no válido. No se puede capturar al rey."

        #6. Comprobación de las reglas de cada pieza:

        #Se llama al método correspondiente al tipo de pieza.
        movimiento_permitido: bool = pieza_origen.es_movimiento_valido(self, origen, destino)

        if not movimiento_permitido:
            return "Movimiento no válido para esta pieza (" + pieza_origen.nombre + ")."

        #7. Comprobación de que no dejamos al rey propio en jaque.

        if self.deja_rey_en_jaque(origen, destino, color_turno):
            return "Movimiento no válido. El rey quedaría en jaque."

        #Si el movimiento supera todas las comprobaciones anteriores, se devuelve un texto vacío para indicar que es válido.
        return ""

    
    def buscar_rey(self, color: str) -> tuple[int, int] | None:
        """Busca el rey del color indicado y devuelve sus coordenadas."""

        for fila in range(TAMANO_TABLERO):
            for columna in range(TAMANO_TABLERO):

                pieza: Pieza | None = self.casillas[fila][columna]

                if pieza is not None:
                    if pieza.nombre == "rey" and pieza.color == color:

                        fila_coordenada: int = TAMANO_TABLERO - 1 - fila

                        return fila_coordenada, columna

        return None


    def casilla_atacada(self, casilla: tuple[int, int], color_atacante: str) -> bool:
        """Comprueba si alguna pieza del color indicado podría atacar cierta casilla."""

        for fila in range(TAMANO_TABLERO):              #Se recorren todas las casillas mediante un bucle.
            for columna in range(TAMANO_TABLERO):

                #Se consulta la piezaque hay en cada casilla.
                pieza: Pieza | None = self.casillas[fila][columna]

                if pieza is not None:
                    if pieza.color == color_atacante:       #Si es del color atacante, se comprueba su movimiento.

                        fila_origen: int = TAMANO_TABLERO - 1 - fila
                        origen: tuple[int, int] = (fila_origen, columna)

                        #Caso peones: ataque diagonal.
                        if pieza.nombre == "peón":

                            if color_atacante == "blanca":
                                direccion: int = 1
                            else:
                                direccion = -1

                            diferencia_filas: int = casilla[0] - origen[0]
                            diferencia_columnas: int = abs(casilla[1] - origen[1])

                            if diferencia_filas == direccion and diferencia_columnas == 1:
                                return True

                        #Otros casos: reglas propias.
                        else:
                            if origen != casilla:
                                if pieza.es_movimiento_valido(self, origen, casilla):
                                    return True

        return False    #Ninguna pieza del color indicado ataca la casilla.


    def esta_en_jaque(self, color: str) -> bool:
        """Comprueba si el rey del color indicado está en jaque."""

        posicion_rey: tuple[int, int] | None = self.buscar_rey(color)

        if posicion_rey is None:
            return False

        if color == "blanca":
            color_atacante: str = "negra"
        else:
            color_atacante = "blanca"

        return self.casilla_atacada(posicion_rey, color_atacante)


    def deja_rey_en_jaque(self, origen: tuple[int, int], destino: tuple[int, int], color: str) -> bool:
        """Simula un movimiento y comprueba si deja al rey propio en jaque."""

        #Convierte las filas a índices de la matriz.
        fila_origen: int = TAMANO_TABLERO - 1 - origen[0]
        fila_destino: int = TAMANO_TABLERO - 1 - destino[0]

        #Guardar las piezas de ambas casillas.
        pieza_origen: Pieza | None = self.casillas[fila_origen][origen[1]]
        pieza_destino: Pieza | None = self.casillas[fila_destino][destino[1]]

        #Simular el movimiento.
        self.casillas[fila_destino][destino[1]] = pieza_origen
        self.casillas[fila_origen][origen[1]] = None

        #Comprobamos si el rey está en jaque.
        rey_en_jaque: bool = self.esta_en_jaque(color)

        #Se restaura el tablero a su posición original.
        self.casillas[fila_origen][origen[1]] = pieza_origen
        self.casillas[fila_destino][destino[1]] = pieza_destino

        return rey_en_jaque


    def tiene_movimientos_validos(self, color: str) -> bool:
        """Comprueba si existe algún movimiento legal para el color indicado."""

        for fila in range(TAMANO_TABLERO):              #Recorre todas las casillas buscando piezas propias.
            for columna in range(TAMANO_TABLERO):

                pieza: Pieza | None = self.casillas[fila][columna]

                if pieza is not None:
                    if pieza.color == color:

                        fila_origen: int = TAMANO_TABLERO - fila        #Convertir la posición de la pieza a una casilla.
                        casilla_origen: str = (LETRAS_VALIDAS[columna] + str(fila_origen))

                        #Probar todos los posibles destinos:
                        for fila_destino in range(TAMANO_TABLERO):
                            for columna_destino in range(TAMANO_TABLERO):

                                casilla_destino: str = (LETRAS_VALIDAS[columna_destino]+ str(TAMANO_TABLERO - fila_destino))
                                movimiento: str = (casilla_origen + " " + casilla_destino)

                                #Se reutiliza el validador completo.
                                motivo: str = self.validar_movimiento(movimiento, color)

                                if motivo == "":
                                    return True

        # Ninguna pieza tiene un movimiento legal.
        return False


def gestionar_turno(tablero: Tablero, color_turno: str) -> str:
    """Pide un movimiento y devuelve el resultado del turno."""

    #Muestra de quién es el turno:
    if color_turno == "blanca":
        print("Es el turno de las blancas.")
    else:
        print("Es el turno de las negras.")

    #Se pide el movimiento o una orden especial.
    texto: str = input("Introduce un movimiento (origen destino), 'exportar' o 'salir': ")

    #Validación de ordenes especiales:
    orden: str = texto.strip().lower()

    if orden == "salir":
        return "salir"
    if orden == "exportar":
        return "exportar"

    #Validación de movimiento introducido.
    motivo: str = tablero.validar_movimiento(texto, color_turno)

    if motivo != "":
        print("Movimiento rechazado:", motivo)
        return "invalido"

    #Si llega aquí, el movimiento es válido.
    movimiento: tuple[str, str] | None = procesar_movimiento(texto)
    if movimiento is None:
        return "invalido"

    casilla_origen: str = movimiento[0]
    casilla_destino: str = movimiento[1]

    origen: tuple[int, int] = convertir_casilla_a_coordenadas(casilla_origen)
    destino: tuple[int, int] = convertir_casilla_a_coordenadas(casilla_destino)

    #Se aplica el movimiento ya validado.
    tablero.mover_pieza(origen, destino)

    print("Movimiento aplicado:", casilla_origen, "->", casilla_destino)

    tablero.imprimir_tablero()

    return "valido"

def comprobar_estado_partida(tablero: Tablero, color: str) -> bool:
    """Anuncia jaque, jaque mate o rey ahogado y devuelve si terminó la partida."""

    en_jaque: bool = tablero.esta_en_jaque(color)
    tiene_movimientos: bool = tablero.tiene_movimientos_validos(color)

    if en_jaque:
        if not tiene_movimientos:
            print("¡Jaque mate!")
            if color == "blanca":
                print("Han ganado las negras.")
            else:
                print("Han ganado las blancas.")
            return True
        print("¡Jaque al rey de las " + color + "s!")

    elif not tiene_movimientos:
        print("¡Rey ahogado!")
        print("La partida termina en tablas.")
        return True

    return False


# __________ Bucle principal: máquina de estados __________

"""El juego utiliza una máquina de estados que alterna entre el turno de las blancas y el turno de las negras."""

def jugar_partida() -> None:
    """Gestiona los turnos y el final de la partida."""

    # ________ Tablero y estado inicial ________

    tablero: Tablero = Tablero()
    tablero.imprimir_tablero()

    estado: str = "turno_blancas"       #El estado inicial de una partida nueva siempre es "turno_blancas".

    while estado != "fin_partida":

        # ________ Turno de las blancas ________
        if estado == "turno_blancas":
            resultado: str = gestionar_turno(tablero, "blanca")     #Muestra de quién es el turno y pide una orden.

            if resultado == "salir":        #Se cambia el estado a "salir" y el bucle termina.
                estado = "fin_partida"
            elif resultado == "valido":    
                partida_terminada: bool = comprobar_estado_partida(tablero, "negra")
                if partida_terminada:
                    estado = "fin_partida"
                else: 
                    estado = "turno_negras"     #Se cambia el estado a "turno_negras".

        # ________ Turno de las negras ________
            #Este bloque funciona como el anterior, y después de una consulta válida devuelve el turno a las blancas.

        elif estado == "turno_negras":
            resultado = gestionar_turno(tablero, "negra")

            if resultado == "salir":
                estado = "fin_partida"
            elif resultado == "valido":
                partida_terminada = comprobar_estado_partida(tablero, "blanca")
                if partida_terminada:
                    estado = "fin_partida"
                else:
                    estado = "turno_blancas"

        # Si el movimiento es inválido, no cambia el estado.

    print("Fin de la partida.")

if __name__ == "__main__":
    jugar_partida()