from typing import Optional

# desabilitando raising-bad-type porque o pylint nao consegue interpretar que as excecoes so serao raised caso not None
# pylint: disable=missing-function-docstring,raising-bad-type,too-many-instance-attributes
class APICotacoesSpy():
    @property
    async def lista_moedas(self) -> list[str]:
        self.__lista_moedas_chamado = True
        if self.excecao_para_raise:
            raise self.excecao_para_raise

        return self.lista_moedas_para_retornar

    @property
    def lista_moedas_chamado(self) -> bool:
        return self.__lista_moedas_chamado

    @property
    def obter_cotacao_chamado(self) -> bool:
        return self.__obter_cotacao_chamado

    @property
    def codigo_moeda_passado_obter_cotacao(self) -> Optional[str]:
        return self.__codigo_moeda_passado_obter_cotacao

    @property
    def recuperar_nome_moeda_chamado(self) -> bool:
        return self.__recuperar_nome_moeda_chamado

    @property
    def codigo_moeda_passado_recuperar_nome_moeda(self) -> Optional[str]:
        return self.__codigo_moeda_passado_recuperar_nome_moeda

    def __init__(self) -> None:
        self.__lista_moedas_chamado = False
        self.__obter_cotacao_chamado = False
        self.__codigo_moeda_passado_obter_cotacao: Optional[str] = None
        self.__recuperar_nome_moeda_chamado = False
        self.__codigo_moeda_passado_recuperar_nome_moeda: Optional[str] = None
        self.lista_moedas_para_retornar: list[str] = []
        self.cotacao_para_retornar = float(0)
        self.excecao_para_raise: Optional[Exception] = None
        self.nome_moeda_para_retornar = ''

    async def obter_cotacao(self, codigo_moeda: str) -> float:
        self.__obter_cotacao_chamado = True
        self.__codigo_moeda_passado_obter_cotacao = codigo_moeda

        if self.excecao_para_raise:
            raise self.excecao_para_raise

        return self.cotacao_para_retornar

    async def recuperar_nome_moeda(self, codigo: str) -> str:
        self.__recuperar_nome_moeda_chamado = True
        self.__codigo_moeda_passado_recuperar_nome_moeda = codigo
        return self.nome_moeda_para_retornar
