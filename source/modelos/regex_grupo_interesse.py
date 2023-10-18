class RegexGrupoInteresse():
    def __init__(self, index: int, tipo: type) -> None:
        """
        Parâmetros:
            - index: índice do grupo de captura do regex.
            - tipo: tipo de dado capturado no índice.
        """
        self.index = index
        self.tipo = tipo
