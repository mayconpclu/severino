from asyncio import AbstractEventLoop

from source.excecoes.expressao_invalida import ExpressaoInvalida
from source.excecoes.falha_download import FalhaDownload
from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.excecoes.moeda_invalida import MoedaInvalida
from source.helpers.api_cotacoes import APICotacoes
from source.helpers.avaliador_regex import AvaliadorRegex
from source.io_manager import IOManager
from source.modelos.habilidade import Habilidade
from source.modelos.regex_grupo_interesse import RegexGrupoInteresse

class HabilidadeConversaoMoeda(Habilidade):
    __REGEX_ACEITACAO = r'^(\d+(\.\d+)?) para ([A-Za-z]+)$'
    __INDEX_QUANTIA = 0
    __INDEX_MOEDA = 2

    @property
    def textos_ajuda(self) -> list[str]:
        try:
            moedas = self.__running_loop.run_until_complete(self.__api.lista_moedas)
            return [
                'Posso converter um valor em Reais para outra moeda usando a cotação atual.',
                '\tO comando é: valor para codigo_moeda. Exempo: \"100 para USD\" converte 100 reais para dólares.',
                '\tA lista de moedas que tenho acesso é:',
            ] + [f'\t\t{moeda}' for moeda in moedas]
        except FalhaDownload:
            return []

    def __init__(self, running_loop: AbstractEventLoop, io_manager: IOManager) -> None:
        self.__running_loop = running_loop
        self.__api = APICotacoes(running_loop)
        self.__io_manager = io_manager
        self.__avaliador_regex = AvaliadorRegex(HabilidadeConversaoMoeda.__REGEX_ACEITACAO, [
            RegexGrupoInteresse(HabilidadeConversaoMoeda.__INDEX_QUANTIA, float),
            RegexGrupoInteresse(HabilidadeConversaoMoeda.__INDEX_MOEDA, str),
        ])

    def execute_ou_raise(self, comando: str) -> None:
        try:
            quantia, moeda = self.__avaliador_regex.avaliar(comando)
            self.__io_manager.imprimir('Vou buscar a cotação atual e fazer a conversão...')
            cotacao = self.__running_loop.run_until_complete(self.__api.obter_cotacao(moeda))
            nome_moeda = self.__running_loop.run_until_complete(self.__api.recuperar_nome_moeda(moeda))
            self.__io_manager.imprimir(f'{round(quantia / cotacao, 2)} {nome_moeda}')
        except ExpressaoInvalida:
            raise FormatoDesconhecido()
        except MoedaInvalida:
            self.__io_manager.imprimir('Moeda inválida. Para obter uma lista de moedas digite ajuda.')
        except FalhaDownload:
            self.__io_manager.imprimir('Algo deu errado. Verifique sua conexão e tente com outra moeda.')
