from threading import Thread
from typing import Callable

from source.helpers.contador_compartilhado import ContadorCompartilhado

HandlerLeitura = Callable[[str], None]

class IOManager():
    COR_CIANO = '\033[96m'
    FIM_COR = '\033[0m'

    def __init__(self) -> None:
        self.__contador_linha = ContadorCompartilhado(1)

    def iniciar(self, handler_leitura: HandlerLeitura) -> None:
        """
        Inicia os serviços de entrada e saída.\n
        Parâmetros:
            - handler_leitura: função callback para ser chamada toda vez que uma leitura é realizada.
        """
        self.__imprime_numero_linha()
        self.__iniciar_leitura(handler_leitura)

    def __imprime_numero_linha(self) -> None:
        linha = self.__contador_linha.recuperar_e_incrementar()
        print(f'{linha:04d} |', end='\t')

    def __iniciar_leitura(self, handler_leitura: HandlerLeitura) -> None:
        thread = Thread(target=self.__executar_leitura, args=[handler_leitura])
        thread.start()

    def __executar_leitura(self, handler_leitura: HandlerLeitura) -> None:
        while True:
            comando = input()
            self.__imprime_numero_linha()
            handler_leitura(comando)

    def imprimir(self, mensagem: str) -> None:
        """
        Imprime a mensagem recebida.
        """
        print(f'{IOManager.COR_CIANO}{mensagem}{IOManager.FIM_COR}')
        self.__imprime_numero_linha()
 