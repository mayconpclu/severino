from asyncio import AbstractEventLoop
from typing import Any

from requests import get, Response

from source.excecoes.falha_download import FalhaDownload
from source.excecoes.moeda_invalida import MoedaInvalida

class APICotacoes():
    __ENDPOINT_LISTA_MOEDAS = 'https://economia.awesomeapi.com.br/json/available/uniq'
    __ENDPOINT_BASE_CONVERSAO = 'https://economia.awesomeapi.com.br/json/last/'
    __CODIGO_MOEDA_REAL = 'BRL'
    __CHAVE_COMPRA = 'ask'

    @property
    async def lista_moedas(self) -> list[str]:
        """
        Propriedade assíncrona que retorna a lista de moedas com informações sobre o código e o nome de cada moeda.
        """
        await self.__task_download_moedas
        return self.__transformar_moedas_em_lista()

    def __transformar_moedas_em_lista(self) -> list[str]:
        return [f'{chave}: {valor}' for chave, valor in self.__moedas.items()]

    def __init__(self, running_loop: AbstractEventLoop) -> None:
        self.__moedas: dict[str, str] = {}
        self.__task_download_moedas = running_loop.run_in_executor(None, self.__download_moedas)

    def __download_moedas(self) -> None:
        moedas_json = dict[str, str](self.__try_download_json(APICotacoes.__ENDPOINT_LISTA_MOEDAS))
        for codigo_moeda, nome_moeda in moedas_json.items():
            self.__adicionar_moeda_se_necessario(codigo_moeda, nome_moeda)

    def __try_download_json(self, endpoint: str) -> Any:
        try:
            resposta = get(endpoint, timeout=10)
            return self.__extrair_json(resposta)
        except Exception:
            raise FalhaDownload()

    def __adicionar_moeda_se_necessario(self, codigo_moeda: str, nome_moeda: str) -> None:
        # Remover Real da lista para nao permitir conversao Real -> Real
        if codigo_moeda.startswith(APICotacoes.__CODIGO_MOEDA_REAL):
            return
        self.__moedas[codigo_moeda] = nome_moeda

    def __extrair_json(self, resposta: Response) -> Any:
        if not resposta.ok:
            raise FalhaDownload()
        return resposta.json()

    async def obter_cotacao(self, codigo_moeda: str) -> float:
        """
        Busca a cotação atual da moeda.\n
        Caso o código recebido seja inválido, a exceção `MoedaInvalida` é lançada.
        """
        codigo = codigo_moeda.upper()
        if not await self.__checar_se_moeda_valida(codigo):
            raise MoedaInvalida()
        endpoint = self.__gerar_endpoint_conversao(codigo)
        resposta_json = dict[str, Any](self.__try_download_json(endpoint))
        return self.__extrair_valor_compra(resposta_json)

    async def __checar_se_moeda_valida(self, codigo_moeda: str) -> bool:
        await self.__task_download_moedas
        return codigo_moeda in self.__moedas

    def __gerar_endpoint_conversao(self, codigo_moeda: str) -> str:
        return APICotacoes.__ENDPOINT_BASE_CONVERSAO + f'{codigo_moeda}-{APICotacoes.__CODIGO_MOEDA_REAL}'

    def __extrair_valor_compra(self, json: dict[str, Any]) -> float:
        json_chave = list(json.keys())[0]
        return float(json[json_chave][APICotacoes.__CHAVE_COMPRA])

    async def recuperar_nome_moeda(self, codigo: str) -> str:
        """
        Retorna o nome da moeda para o código recebido.\n
        Lança a exceção `MoedaInvalida` caso a moeda não seja encontrada.
        """
        codigo_moeda = codigo.upper()
        if not await self.__checar_se_moeda_valida(codigo_moeda):
            raise MoedaInvalida()
        return self.__moedas[codigo_moeda]
