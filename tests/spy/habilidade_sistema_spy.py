from typing import Optional

from source.modelos.habilidade import Habilidade

class HabilidadeSistemaSpy(Habilidade):
    @property
    def textos_ajuda(self) -> list[str]:
        return self.textos_para_retornar

    @property
    def execute_ou_raise_chamado(self) -> bool:
        return self.__execute_ou_raise_chamado

    @property
    def comando_passado(self) -> Optional[str]:
        return self.__comando_passado

    def __init__(self) -> None:
        self.textos_para_retornar: list[str] = []
        self.__execute_ou_raise_chamado = False
        self.__comando_passado: Optional[str] = None

    def execute_ou_raise(self, comando: str) -> None:
        self.__execute_ou_raise_chamado = True
        self.__comando_passado = comando
