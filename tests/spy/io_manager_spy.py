from typing import Optional

from source.io_manager import IOManager, HandlerLeitura

# pylint: disable=missing-function-docstring
class IOManagerSpy(IOManager):
    @property
    def iniciar_chamado(self) -> bool:
        return self.__iniciar_chamado

    @property
    def handler_leitura_passado(self) -> Optional[HandlerLeitura]:
        return self.__handler_leitura_passado

    @property
    def imprimir_chamado_count(self) -> int:
        return self.__imprimir_chamado_count

    @property
    def mensagens_passadas(self) -> list[str]:
        return self.__mensagens_passadas

    # desabilitando regra porque nao queremos inicializar a classe pai
    # pylint: disable=super-init-not-called
    def __init__(self) -> None:
        self.__iniciar_chamado = False
        self.__handler_leitura_passado: Optional[HandlerLeitura] = None
        self.__imprimir_chamado_count = 0
        self.__mensagens_passadas: list[str] = []

    def iniciar(self, handler_leitura: HandlerLeitura) -> None:
        self.__iniciar_chamado = True
        self.__handler_leitura_passado = handler_leitura

    def imprimir(self, mensagem: str) -> None:
        self.__imprimir_chamado_count += 1
        self.__mensagens_passadas.append(mensagem)
