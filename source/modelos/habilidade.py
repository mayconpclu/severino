from abc import ABC, abstractmethod

class Habilidade(ABC):
    @property
    @abstractmethod
    def textos_ajuda(self) -> list[str]:
        """
        Retorna os textos de ajuda para a Habilidade.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute_ou_raise(self, comando: str) -> None:
        """
        Executa o comando caso o conheça.\n
        Caso contrário, lança a exceção `FormatoDesconhecido`.
        """
        raise NotImplementedError()
