from threading import Lock

class ContadorCompartilhado():
    def __init__(self, valor_inicial: int = 0) -> None:
        self.__valor = valor_inicial
        self.__lock = Lock()

    def recuperar(self) -> int:
        """
        Retorna o valor atual, de maneira thread-safe.
        """
        with self.__lock:
            return self.__valor

    def incrementar(self) -> None:
        """
        Incrementa o valor atual em 1, de maneira thread-safe.
        """
        with self.__lock:
            self.__valor += 1

    def recuperar_e_incrementar(self) -> int:
        """
        Retorna o valor atual e o incrementa em 1, de maneira thread-safe.
        """
        with self.__lock:
            valor = self.__valor
            self.__valor += 1
        return valor
