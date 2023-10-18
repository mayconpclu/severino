from asyncio import get_event_loop
from typing import Optional

from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.habilidades.habilidade_calculadora import HabilidadeCalculadora
from source.habilidades.habilidade_conversao_moedas import HabilidadeConversaoMoeda
from source.habilidades.habilidade_sistema import HabilidadeSistema
from source.io_manager import IOManager
from source.modelos.habilidade import Habilidade

class Severino:
    def __init__(self) -> None:
        self.__running_loop = get_event_loop()
        self.__io_manager = IOManager()
        self.__habilidade_sistema = HabilidadeSistema(self.__io_manager, self.__get_textos_ajuda)
        self.__habilidades: list[Habilidade] = [self.__habilidade_sistema]
        self.__comando_para_executar: Optional[str] = None

        self.__iniciar_servicos()
        self.__imprimir_mensagem_inicial()

    def __iniciar_servicos(self) -> None:
        self.__io_manager.iniciar(self.__handler_leitura_recebida)
        self.__habilidades.extend([
            HabilidadeCalculadora(self.__io_manager),
            HabilidadeConversaoMoeda(self.__running_loop, self.__io_manager),
        ])

    def __imprimir_mensagem_inicial(self) -> None:
        self.__io_manager.imprimir('Sou o Severino, o seu faz-quase-tudo.')
        for mensagem in self.__habilidade_sistema.textos_ajuda:
            self.__io_manager.imprimir(f'- {mensagem}')

    def __handler_leitura_recebida(self, comando: str) -> None:
        self.__comando_para_executar = comando
        for habilidade in self.__habilidades:
            self.__execute_comando_se_possivel(habilidade)

        self.__imprimir_comando_invalido_se_necessario()

    def __get_textos_ajuda(self) -> list[str]:
        resultado: list[str] = []
        for mensagens in [habilidade.textos_ajuda for habilidade in self.__habilidades]:
            resultado.extend(mensagens)
        return resultado

    def __execute_comando_se_possivel(self, habilidade: Habilidade) -> None:
        if not self.__comando_para_executar:
            return

        try:
            habilidade.execute_ou_raise(self.__comando_para_executar)
            self.__comando_para_executar = None
        except FormatoDesconhecido:
            pass

    def __imprimir_comando_invalido_se_necessario(self) -> None:
        if self.__comando_para_executar:
            self.__io_manager.imprimir('Não conheço esse comando.')

        self.__comando_para_executar = None
