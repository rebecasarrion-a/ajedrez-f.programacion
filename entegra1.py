estado: str = "turno_blancas"
while estado != "salir":
    if estado == "turno_blancas":
        print("Es el turno de las blancas")
    elif estado == "turno_negras":
        print("Es el turno de las negras")