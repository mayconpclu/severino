from sys import exit as sys_exit
from typing import Callable

from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.modelos.habilidade import Habilidade
from source.io_manager import IOManager

class HabilidadeSistema(Habilidade):
    @property
    def textos_ajuda(self) -> list[str]:
        return [
            'Digite ajuda para ver o que eu posso fazer.',
            'Digite sair para encerrar.',
        ]

    def __init__(self, io_manager: IOManager, get_textos_ajuda: Callable[[], list[str]]) -> None:
        self.__io_manager = io_manager
        self.__get_textos_ajuda = get_textos_ajuda

    def execute_ou_raise(self, comando: str) -> None:
        match (comando):
            case 'ajuda': self.__executa_ajuda()
            case 'sair': self.__sair()
            case _: raise FormatoDesconhecido()

    def __executa_ajuda(self) -> None:
        for mensagem in self.__get_textos_ajuda():
            self.__io_manager.imprimir(f'- {mensagem}')

    def __sair(self) -> None:
        self.__io_manager.imprimir('Até mais!')
        sys_exit(0)
