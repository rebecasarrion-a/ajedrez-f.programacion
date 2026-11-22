"""
Entrega 2 - Piezas que se mueven

Programa principal de una partida de ajedrez entre
dos jugadores la consola.

La función jugar_partida() inicia y controla la partida..
"""

# __________ Constantes del tablero __________

TAMANO_TABLERO: int = 8     #El tablero tiene 8 filas y 8 columnas.
LETRAS_VALIDAS: str = "abcdefgh"    #Las columnas se identifican con las letras de la 'a' a la 'h'.
NUMEROS_VALIDOS: str = "12345678"    #Las filas se identifican con los números de la '1' a la '8'.
CASILLA_VACIA: str = "·"    #Símbolo que representa una casilla vacía en el tablero.


# __________ Casilla: funciones __________

# ________ Representación de una casilla ________

def convertir_casilla(casilla: str) -> tuple[int, int]:
    """Convierte una casilla "letra número" en una tupla (fila, columna)."""

    fila: int = int(casilla[1]) - 1     #Se resta 1 al número de la casilla para adaptar la numeración del ajedrez (1-8) a los índices internos (0-7).
    columna: int = LETRAS_VALIDAS.index(casilla[0])     #index() busca la letra y devuelve su posición dentro de LETRAS_VALIDAS (0-7).

    return fila, columna    #Devuelve una coordenada (fila, columna).

# ________ Comprobación de una casilla ________

def es_casilla_valida(casilla: str) -> bool:
    """Comprueba si el texto recibido representa una casilla válida del tablero."""

    if len(casilla) != 2:   #Debe tener exactamente dos caracteres.
        return False

    if casilla[0] not in LETRAS_VALIDAS:    #El primero, una letra (columna) de LETRAS_VALIDAS.
        return False

    if casilla[1] not in NUMEROS_VALIDOS:   #El segundo, un número (fila) de NUMEROS_VALIDAS.
        return False

    return True     #Si no se ha rechazado antes, la casilla es válida.

# ________ Formato de un movimiento ________

def procesar_movimiento(texto: str) -> tuple[str, str] | None:
    """Limpia y comprueba la validez del formato de un movimiento introducido."""

    #Con el texto introducido:
    movimiento: str = texto.strip().lower()   #strip() quita espacios al principio y al final; lower() admite letras mayúsculas.
    partes: list[str] = movimiento.split()    #split() separa las dos casillas, aunque haya varios espacios entre ellas.

    #El movimiento debe contener exactamente dos partes (origen y destino).
    if len(partes) != 2:    
        return None         #None indica que el formato no es válido.

    #Se comprueba por separado que origen y destino sean casillas existentes.
    origen: str = partes[0]
    destino: str = partes[1]

    if not es_casilla_valida(origen) or not es_casilla_valida(destino):
        return None

    #Se devuelven las dos casillas ya normalizadas.
    return origen, destino


# __________ Pieza: clase, método y subclases __________

class Pieza:
    """Pieza de ajedrez genérica."""

    def __init__(self, color: str, símbolo: str, nombre: str) -> None:
        self.color: str = color
        self.simbolo: str = símbolo
        self.nombre: str = nombre

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """True si la pieza puede ir de origen a destino según sus reglas.""" 
        return False    #Cada subclase definirá este método con sus reglas.

# ________ Subclases: movimientos validos ________

class Torre(Pieza):
    """Se mueve en línea recta por filas o columnas."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea en línea recta y no haya piezas en el camino."""

        if origen[0] != destino[0] and origen[1] != destino[1]:     #No puede cambiar de fila y columna a la vez.
            return False
        
        return tablero.camino_libre(origen, destino)    #Se comprueba que el trayecto esté vacío.
    
class Caballo(Pieza):
    """Se mueve en forma de L y puede saltar por encima de otras piezas."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento tenga forma de L."""

        #abs() permite medir el desplazamiento sin importar el sentido de este.
        diferencia_filas: int = abs(destino[0] - origen[0])
        diferencia_columnas: int = abs(destino[1] - origen[1])

        #Las dos combinaciones posibles forman la L del caballo.
        if not ((diferencia_filas == 2 and diferencia_columnas == 1) or
                (diferencia_filas == 1 and diferencia_columnas == 2)):
            return False
        
        return True

class Alfil(Pieza):
    """Se mueve en diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea en diagonal y no hay piezas en el camino."""

        #En una diagonal se avanza el mismo número de filas que de columnas.
        if abs(destino[0] - origen[0]) != abs(destino[1] - origen[1]):     #abs() compara distancias sin importar el sentido.
            return False

        return tablero.camino_libre(origen, destino)    #Se comprueba que la diagonal esté vacía.

class Dama(Pieza):
    """Se mueve en horizontal, vertical o diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que el desplazamiento sea horizontal, vertical o diagonal y no haya piezas en el camino."""

        #Definición de los movimientos permitidos:
        movimiento_recto: bool = (origen[0] == destino[0] or origen[1] == destino[1])
        movimiento_diagonal: bool = (abs(destino[0] - origen[0]) == abs(destino[1] - origen[1]))

        if not movimiento_recto and not movimiento_diagonal:
            return False

        return tablero.camino_libre(origen, destino)    #Si comprueba que el trayecto esté vacío.

class Rey(Pieza):
    """Se mueve una casilla, en cualquier dirección."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que se desplace una sola casilla."""

        if abs(destino[0] - origen[0]) > 1 or abs(destino[1] - origen[1]) > 1:
            return False
        else:
            return True     #Si las distancias son 1, el movimiento es permitido.

class Peón(Pieza):
    """Se mueve una casilla hacia delante (dos si es primer movimiento) y captura una casilla en diagonal."""

    def es_movimiento_valido(self, tablero: "Tablero", origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Siempre que se desplace una casilla hacia delante, dos si es el primer movimiento, y capture una casilla en diagonal."""

        #Dirección de avance según color:

        if self.color == "blanca":  #Las blancas avanzan hacia números de fila mayores.
            direccion: int = 1
            fila_inicial: int = 1
        else:                       #Las negras avanzan hacia números de fila menores
            direccion = -1
            fila_inicial = 6

        #Se calculan los desplazamientos para distinguir avance y captura.
        diferencia_filas: int = destino[0] - origen[0]
        diferencia_columnas: int = abs(destino[1] - origen[1])

        fila_destino_tablero: int = TAMANO_TABLERO - 1 - destino[0]     #Conversión de la fila al índice de la matriz (fila 8 arriba, fila 1 abajo).

        #Consulta de pieza en la casilla de destino.
        pieza_destino: Pieza | None = tablero.casillas[fila_destino_tablero][destino[1]]

        # __ CASO GENERAL: avanzar una casilla hacia delante (con destino vacío) __
        
        if diferencia_filas == direccion and diferencia_columnas == 0:
            if pieza_destino is None:
                return True
            else:
                return False

        # __ CASO PRIMER MOVIMIENTO: avanzar dos casillas hacia delante (con destino vacío) __
        
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
        
        if diferencia_filas == direccion and diferencia_columnas == 1:      
            if pieza_destino is not None and pieza_destino.color != self.color:   #Solo se permite capturar a una pieza del color rival.
                return True
            else:
                return False

        #Cualquier otro desplazamiento queda descartado.
        return False


# __________ Tablero __________

class Tablero:
    """Guarda la posición de las piezas y las operaciones sobre el tablero."""

    def __init__(self) -> None:
        self.casillas: list[list[Pieza | None]] = [         #Construye una lista de listas: cada lista interior representa una fila y None indica una casilla vacía..
            [None for _ in range(TAMANO_TABLERO)]
            for _ in range(TAMANO_TABLERO)
        ]

        self.colocar_posicion_inicial()                     #La rellena con las piezas en su posición inicial.

# _____ Métodos _____

    def colocar_posicion_inicial(self) -> None:
        """Coloca todas las piezas en sus posiciones iniciales."""

        piezas_blancas: list[tuple[str, str]] = [
            ("torre", "♖"), ("caballo", "♘"), ("alfil", "♗"), ("dama", "♕"),
            ("rey", "♔"), ("alfil", "♗"), ("caballo", "♘"), ("torre", "♖")
        ]

        piezas_negras: list[tuple[str, str]] = [
            ("torre", "♜"), ("caballo", "♞"), ("alfil", "♝"), ("dama", "♛"),
            ("rey", "♚"), ("alfil", "♝"), ("caballo", "♞"), ("torre", "♜")
        ]

        #Variables que guardan el nombre y el símbolo de cada pieza al recorrer las listas.
        nombre: str
        simbolo: str

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
                pieza: Pieza | None = self.casillas[fila][columna]      #Una casilla puede contener un objeto Pieza o estar vacía.

                if pieza is None:
                    print("·", end=" ")
                else:
                    print(pieza.simbolo, end=" ")

            print()     #Al terminar cada fila, se pasa a la línea siguiente.

        print()  #Línea en blanco después del tablero.


    def mover_pieza(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Mueve una pieza desde la casilla de origen hasta la casilla de destino."""

        #Se separa las coordenadas para acceder a las casillas de la matriz.
        fila_origen: int = origen[0]
        columna_origen: int = origen[1]

        fila_destino: int = destino[0]
        columna_destino: int = destino[1]

        #Conversión de filas a los índices de la matriz.
        fila_origen_tablero: int = TAMANO_TABLERO - 1 - fila_origen
        fila_destino_tablero: int = TAMANO_TABLERO - 1 - fila_destino

    #El movimiento no se realiza cuando:
       
       #El origen y el destino son los mismos.
        if origen == destino:
            return False

        #La casilla de origen está vacía.
        pieza: Pieza | None = self.casillas[fila_origen_tablero][columna_origen]
        if pieza is None:
            return False

    #Una vez superadas estas comprobaciones, se actualizan las casillas.
    
        self.casillas[fila_destino_tablero][columna_destino] = pieza    #La pieza del origen sustituye a la del destino.
        self.casillas[fila_origen_tablero][columna_origen] = None       #Se vacía la casilla de origen.

         # _____ Coronación automática del peón _____

        if pieza.nombre == "peón":      #Si la pieza movida es un peón:

            if pieza.color == "blanca" and destino[0] == 7:                                             #Si es blanco y llega a la fila 8,
                self.casillas[fila_destino_tablero][columna_destino] = Dama("blanca", "♕", "dama")     #se sustituye automáticamente por una dama del mismo color.
                print("¡El peón blanco ha coronado a dama!")

            elif pieza.color == "negra" and destino[0] == 0:                                            #Si es negro y llega a la fila 1,
                self.casillas[fila_destino_tablero][columna_destino] = Dama("negra", "♛", "dama")      #se sustituye automáticamente por una dama del mismo color.
                print("¡El peón negro ha coronado a dama!")

        return True


    def camino_libre(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Comprueba si las casillas situadas entre el origen y el destino están vacías."""

        #El valor de las diferencias entre filas indica que:
        diferencia_filas: int = destino[0] - origen[0]
        if diferencia_filas > 0:    
            paso_fila: int = 1        #Se avanza de fila en fila hacia arriba.
        elif diferencia_filas < 0:
            paso_fila: int = -1       #Se retrocede de fila en fila hacia abajo.
        else:
            paso_fila: int = 0        #No se cambia de fila.

        #El valor de las diferencias entre columnas indica que:
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

        while (fila_actual, columna_actual) != destino:     #El bucle revisa solo las casillas intermedias: el destino puede contener una pieza rival.

            fila_tablero: int = TAMANO_TABLERO - 1 - fila_actual    #Conversión de la fila al índice de la matriz.
            
            #Se consulta si la casilla intermedia está ocupada.
            pieza: Pieza | None = self.casillas[fila_tablero][columna_actual]
            if pieza is not None:
                return False             #Si hay una pieza, termina el método.

            #Si está vacía, avanza a la siguiente.
            fila_actual = fila_actual + paso_fila           
            columna_actual = columna_actual + paso_columna

        #Si se llega al destino sin encontrar obstáculos, el camino está libre.
        return True


    def validar_movimiento(self, texto: str, color_turno: str) -> str:
        """Comprueba si un movimiento es válido para el jugador al que le corresponde el turno y explica el primer motivo de rechazo."""

        #1. Comprobación del formato:
        movimiento: tuple[str, str] | None = procesar_movimiento(texto)

        if movimiento is None:
            return "Formato no válido. Escribe origen y destino, por ejemplo: e2 e4."

            #Separamos las dos casillas que devuelve procesar_movimiento().
        casilla_origen: str = movimiento[0]
        casilla_destino: str = movimiento[1]
            #Convertimos ambas casillas a coordenadas (fila, columna).
        origen: tuple[int, int] = convertir_casilla(casilla_origen)
        destino: tuple[int, int] = convertir_casilla(casilla_destino)

        #2. Comprobación de origen y destino iguales:
        if origen == destino:
            return "El origen y el destino son iguales. La pieza no se mueve."

        #3. Comprobación de que hay una pieza en el origen:
        fila_origen_tablero: int = TAMANO_TABLERO - 1 - origen[0]   #Conversión de la fila al índice de la matriz.

        pieza_origen: Pieza | None = self.casillas[fila_origen_tablero][origen[1]]

        if pieza_origen is None:
            return "No hay ninguna pieza en la casilla de origen."

        #4. Comprobación del color del turno:
        if pieza_origen.color != color_turno:                               #Solo se permite mover piezas del jugador en turno.
            return "No es tu turno, es el de las " + color_turno + "s."

        #5. Comprobación de piezas que no se pueden capturar: del mismo color y rey.
        fila_destino_tablero: int = TAMANO_TABLERO - 1 - destino[0]         #Conversión de la fila al índice de la matriz.

        pieza_destino: Pieza | None = self.casillas[fila_destino_tablero][destino[1]]       #Consulta de pieza en el destino.

        if pieza_destino is not None:
            if pieza_destino.color == color_turno:      #Si hay una, no puede ser del mismo color de las piezas en turno.
                return "La casilla de destino está ocupada por una pieza propia."
            if pieza_destino.nombre == "rey":           #Si hay una, no puede ser un rey (no se captura, es jaque mate y termina la partida).
                return "No se puede capturar al rey."

        #6. Comprobación de las reglas de cada tipo de pieza:

        #Se llama al método correspondiente al tipo de pieza.
        movimiento_permitido: bool = pieza_origen.es_movimiento_valido(self, origen, destino)

        if not movimiento_permitido:
            return "No es válido para esta pieza (" + pieza_origen.nombre + ")."

        #7. Comprobación de no dejar al rey propio en jaque.

        if self.deja_rey_en_jaque(origen, destino, color_turno):
            return "Ese movimiento deja a tu propio rey en jaque."

        #Una cadena vacía indica que no hay motivo para rechazar el movimiento.
        return ""

    
    def buscar_rey(self, color: str) -> tuple[int, int] | None:
        """Busca el rey del color indicado y devuelve sus coordenadas."""

        #El bucle reccorre todas las casillas de la matriz hasta encontrar una pieza cuyo nombre sea "rey" y cuyo color sea el solicitado.
        for fila in range(TAMANO_TABLERO):
            for columna in range(TAMANO_TABLERO):

                pieza: Pieza | None = self.casillas[fila][columna]

                if pieza is not None:
                    if pieza.nombre == "rey" and pieza.color == color:

                        fila_coordenada: int = TAMANO_TABLERO - 1 - fila     #La matriz se recorre de arriba abajo, pero las coordenadas del juego cuentan desde la fila inferior.

                        return fila_coordenada, columna

        #Si se recorre el tablero sin encontrarlo, no hay posición.
        return None


    def casilla_atacada(self, casilla: tuple[int, int], color_atacante: str) -> bool:
        """Comprueba si alguna pieza del color indicado podría atacar cierta casilla."""

        for fila in range(TAMANO_TABLERO):              #Se recorren todas las casillas mediante un bucle.
            for columna in range(TAMANO_TABLERO):

                #Se consulta qué pieza ocupa cada casilla.
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

        return False     #Si ninguna pieza puede llegar a esa casilla, no está atacada.


    def esta_en_jaque(self, color: str) -> bool:
        """Comprueba si el rey del color indicado está en jaque."""

        posicion_rey: tuple[int, int] | None = self.buscar_rey(color)   #Se localiza al rey con la función buscar_rey.
        
        if posicion_rey is None:
            return False                                                #Si no se encuentra, no hay casilla que comprobar.

        #El atacante siempre será el color contrario al del rey.
        if color == "blanca":
            color_atacante: str = "negra"
        else:
            color_atacante = "blanca"

        #Si alguna pieza rival puede atacar esa casilla, hay jaque.
        return self.casilla_atacada(posicion_rey, color_atacante)


    def deja_rey_en_jaque(self, origen: tuple[int, int], destino: tuple[int, int], color: str) -> bool:
        """Simula un movimiento y comprueba si deja al rey propio en jaque."""

        #Convierte las filas a índices de la matriz.
        fila_origen: int = TAMANO_TABLERO - 1 - origen[0]
        fila_destino: int = TAMANO_TABLERO - 1 - destino[0]

        #Guardar las piezas de ambas casillas para poder deshacer la simulación.
        pieza_origen: Pieza | None = self.casillas[fila_origen][origen[1]]
        pieza_destino: Pieza | None = self.casillas[fila_destino][destino[1]]

        #Aplicación del movimiento, sin modificar el historial.
        self.casillas[fila_destino][destino[1]] = pieza_origen
        self.casillas[fila_origen][origen[1]] = None

        #Se comprueba si el rey está en jaque con el tablero simulado.
        rey_en_jaque: bool = self.esta_en_jaque(color)

        #Se recupera la posición anterior, independientemente del resultado.
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

        #Si ninguna combinación es válida, el jugador no puede mover.
        return False


# __________ Partida: funciones __________


import os       #Permite comprobar si existe el archivo de una partida guardada.
import csv      #Permite exportar el historial de movimientos a un archivo CSV.


def guardar_historial(movimientos: list[str], ruta: str) -> None:
    """Guarda la lista de movimientos en un fichero, uno por línea."""

    with open(ruta, "w") as fichero:
        for movimiento in movimientos:
            fichero.write(movimiento + "\n")


def cargar_historial(ruta: str) -> list[str]:
    """Carga el historial de movimientos desde un fichero, si existe."""

    movimientos: list[str] = []
    if os.path.exists(ruta):                #Solo se intenta leer el archivo si existe.
        with open(ruta, "r") as fichero:
            for linea in fichero:
                movimiento: str = linea.strip()
                if movimiento != "":
                    movimientos = movimientos + [movimiento]

    return movimientos


def exportar_historial_csv(movimientos: list[str], ruta: str) -> None:
    """Exporta el historial con número, turno, origen y destino de cada movimiento a CSV."""

    #Se abre el archivo CSV para en modo escritura. Si ya existe, se sustituye su contenido.
    with open(ruta, "w", newline="") as fichero:                        #newline="" evita líneas vacías adicionales entre los movimientos.
        escritor = csv.writer(fichero)                                  #Se prepara el archivo para escribir los datos organizados.
        escritor.writerow(["numero", "turno", "origen", "destino"])     #Se escribe primera fila: cabecera con el nombre de las cuatro columnas.

        #Se recorre el historial para exportar cada movimiento en una fila diferente.
        for indice in range(len(movimientos)):
            numero: int = indice + 1            #Se suma 1 al índice para numerar los movimientos desde 1 y las listas desde 0.
            if indice % 2 == 0:
                turno: str = "blancas"          #Los impares corresponden a las blancas.
            else:
                turno: str = "negras"           #Los pares corresponden a las negras.

            #Variables que guardan las casillas de origen y destino de cada movimiento.
            origen: str
            destino: str

            origen, destino = movimientos[indice].split()           #Se obtiene el movimiento del historial y se separa (.split()).
            escritor.writerow([numero, turno, origen, destino])     #Se escribe una fila con los cuatro datos del movimiento.


def reconstruir_tablero(tablero: Tablero, movimientos: list[str]) -> str:
    """Reproduce los movimientos guardados y comprueba si el historial es válido, inválido o la partida terminó."""

    for indice in range(len(movimientos)):
        movimiento: str = movimientos[indice]       #Se recupera cada movimiento en el orden guardado.

        if indice % 2 == 0:
            color_turno: str = "blanca"
            color_siguiente: str = "negra"
        else:
            color_turno = "negra"
            color_siguiente = "blanca"

        #Cada movimiento debe respetar las reglas y el turno correspondiente.
        if tablero.validar_movimiento(movimiento, color_turno) != "":
            return "invalida"

        casillas: tuple[str, str] | None = procesar_movimiento(movimiento)
        if casillas is None:
            return "invalida"

        origen: tuple[int, int] = convertir_casilla(casillas[0])
        destino: tuple[int, int] = convertir_casilla(casillas[1])
        tablero.mover_pieza(origen, destino)

        #No puede haber movimientos posteriores a una posición final.
        if not tablero.tiene_movimientos_validos(color_siguiente):
            if indice != len(movimientos) - 1:
                return "invalida"
            return "terminada"

    return "valida"


def gestionar_turno(tablero: Tablero, color_turno: str,  historial: list[str]) -> str:
    """Pide un movimiento y devuelve el resultado del turno."""

    #Muestra de quién es el turno:
    if color_turno == "blanca":
        print("Turno de las blancas")
    else:
        print("Turno de las negras")

    #Se pide el movimiento o una orden especial.
    texto: str = input("Introduce un movimiento (origen destino), 'exportar' o 'salir': ")

    #Validación de ordenes especiales:
    orden: str = texto.strip().lower()      #Las órdenes especiales no consumen turno.

    if orden == "salir":
        return "salir"
    if orden == "exportar":
        return "exportar"

    #Validación de movimiento introducido.
    motivo: str = tablero.validar_movimiento(texto, color_turno)

    if motivo != "":
        print()
        print("Movimiento rechazado:", motivo)
        print()
        return "invalido"

    #Solo se continúa si la validación no ha encontrado errores.
    movimiento: tuple[str, str] | None = procesar_movimiento(texto)
    if movimiento is None:
        return "invalido"

    casilla_origen: str = movimiento[0]
    casilla_destino: str = movimiento[1]

    origen: tuple[int, int] = convertir_casilla(casilla_origen)
    destino: tuple[int, int] = convertir_casilla(casilla_destino)

    #Se actualiza el tablero y se registra el movimiento.
    tablero.mover_pieza(origen, destino)

    historial.append(casilla_origen + " " + casilla_destino)
    guardar_historial(historial, "partida.txt")

    print("Movimiento aplicado:", casilla_origen, "->", casilla_destino)

    print()
    print("________________________________")
    print()

    tablero.imprimir_tablero()  #Se imprime el tablero con la nueva posición.

    return "valido"

def comprobar_estado_partida(tablero: Tablero, color: str) -> bool:
    """Anuncia jaque, jaque mate o rey ahogado y devuelve si terminó la partida."""

    #Para distinguir los tres casos se comprueba si su rey está atacado y si dispone de algún movimiento legal.
    en_jaque: bool = tablero.esta_en_jaque(color)
    tiene_movimientos: bool = tablero.tiene_movimientos_validos(color)

    if en_jaque:                                            #Rey atacado:
        if not tiene_movimientos:                           #- Sin movimientos: jaque mate; gana el rival.
            print("Jaque mate.")
            if color == "blanca":
                print("Ganan las negras.")
            else:
                print("Ganan las blancas.")
            return True
        print("Jaque a las " + color + "s.")       #- Si puede defenderse, la partida continúa, pero se avisa del jaque.

    elif not tiene_movimientos:                             #Sin jaque y sin movimientos legales: rey ahogado, que son tablas.
        if color == "blanca":
            print("¡Rey blanco ahogado!")
        else:
            print("¡Rey negro ahogado!")

        print("La partida termina en tablas.")
        return True

    return False    #Si hay movimientos disponibles, la partida todavía no ha terminado.


# __________ Bucle principal: máquina de estados __________

"""El juego utiliza una máquina de estados que alterna los turnos y termina cuando se acaba la partida o se elige salir."""

def jugar_partida() -> None:
    """Gestiona los turnos y el final de la partida."""

    # ________ Tablero e historial inicial ________

    #Se parte de un tablero nuevo y de una lista de movimientos vacía.
    tablero: Tablero = Tablero()
    historial: list[str] = []
    
    # _____ Elegir partida nueva o cargar una guardada _____

    #Si hay una partida guardada, se ofrece recuperarla antes de empezar.
    if os.path.exists("partida.txt"):
        opcion: str = input("¿Quieres cargar una partida guardada? (s/n): ").strip().lower()
    
        if opcion == "s" or opcion == "si" or opcion == "sí":
            historial = cargar_historial("partida.txt")                      #Se leen los movimientos guardados y se reproducen en orden.
            resultado_carga: str = reconstruir_tablero(tablero, historial)

            #Un historial ilegal o una partida ya finalizada no se continúa:se crea otro tablero y se borra el historial recuperado.
            if resultado_carga == "invalida":
                print()
                print("El archivo guardado no es válido. Se inicia una partida nueva.")
                tablero = Tablero()
                historial = []
            elif resultado_carga == "terminada":
                print()
                print("La partida guardada ya había terminado. Se inicia una partida nueva.")
                tablero = Tablero()
                historial = []
            else:
                print()
                print("Partida cargada correctamente.")

    # _____ Mostrar tablero y mensaje de inicio _____

    print()

    if len(historial) == 0:
        print("Comienza una nueva partida. ¡Mucha suerte!")
    else:
        print("¡Que continúe la partida!")

    print()
    tablero.imprimir_tablero()      #Se enseña la posición inicial o la reconstruida desde el archivo.

    # _____ Recuperar el turno _____

    estado: str = "turno_blancas"   #Las blancas empiezan.
    if len(historial) % 2 != 0:     #Un historial impar indica que siguen las negras.
        estado = "turno_negras"

    #El bucle continúa hasta detectar el final de la partida.
    while estado != "fin_partida":

        # ________ Turno de las blancas ________
        if estado == "turno_blancas":
            resultado: str = gestionar_turno(tablero, "blanca", historial)     #Muestra de quién es el turno y pide una orden.

            if resultado == "salir":
                estado = "fin_partida"

            elif resultado == "exportar":
                exportar_historial_csv(historial, "partida.csv")
                print("________________________________")
                print()
                print("Historial exportado a partida.csv.")
                print("________________________________")
                print()
                
            elif resultado == "valido":    
                partida_terminada: bool = comprobar_estado_partida(tablero, "negra")     #Movimiento válido obliga a comprobar la situación del rival.

                if partida_terminada:
                    estado = "fin_partida"
                else: 
                    estado = "turno_negras"     #Se cambia el estado a "turno_negras" después de un movimiento válido.

        # ________ Turno de las negras ________
        #La misma lógica se aplica a las negras.

        elif estado == "turno_negras":
            resultado = gestionar_turno(tablero, "negra", historial)

            if resultado == "salir":
                estado = "fin_partida"

            elif resultado == "exportar":
                exportar_historial_csv(historial, "partida.csv")
                print("________________________________")
                print()
                print("Historial exportado a partida.csv.")
                print("________________________________")
                print()

            elif resultado == "valido":
                partida_terminada = comprobar_estado_partida(tablero, "blanca")

                if partida_terminada:
                    estado = "fin_partida"
                else:
                    estado = "turno_blancas"

        #Si gestionar_turno devuelve "invalido", no se entra en ninguna rama anterior: el estado no cambia y vuelve a jugar el mismo color.

    print()
    print("________________________________")
    print()
    print("Fin de la partida. ¡Hasta la próxima!")      #Mensaje impreso al acabar la partida.
    print()

#La partida comienza cuando se ejecuta directamente el archivo Python.
if __name__ == "__main__":
    jugar_partida()