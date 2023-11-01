from asyncio import new_event_loop
from typing import Any

from source.excecoes.falha_download import FalhaDownload
from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.excecoes.moeda_invalida import MoedaInvalida
from source.habilidades.habilidade_conversao_moedas import HabilidadeConversaoMoeda
from tests.tests_dsl import replace, assert_should_raise
from tests.spy.api_cotacoes_spy import APICotacoesSpy
from tests.spy.io_manager_spy import IOManagerSpy

# pylint: disable=missing-function-docstring
class TestHabilidadeConversaoMoeda():
    __running_loop = new_event_loop()

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy, lambda mock_init: mock_init.assert_called_once_with(TestHabilidadeConversaoMoeda.__running_loop))
    def test_init_deve_passar_running_loop_para_api(self, _: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_textos_ajuda_com_falha_no_download_deve_retornar_vazio(self, api_spy: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        api_spy.excecao_para_raise = FalhaDownload()
        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        textos = habilidade.textos_ajuda

        assert io_manager_spy.iniciar_chamado is False
        assert io_manager_spy.handler_leitura_passado is None
        assert io_manager_spy.imprimir_chamado_count == 0
        assert not io_manager_spy.mensagens_passadas
        assert api_spy.lista_moedas_chamado is True
        assert api_spy.obter_cotacao_chamado is False
        assert api_spy.recuperar_nome_moeda_chamado is False
        assert textos == []

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_textos_ajuda_deve_retornar_textos_de_ajuda(self, api_spy: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        api_spy.lista_moedas_para_retornar = ['FOO: Moeda Foo', 'BAR: Moeda Bar']
        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        textos = habilidade.textos_ajuda

        assert io_manager_spy.iniciar_chamado is False
        assert io_manager_spy.handler_leitura_passado is None
        assert io_manager_spy.imprimir_chamado_count == 0
        assert not io_manager_spy.mensagens_passadas
        assert api_spy.lista_moedas_chamado is True
        assert api_spy.obter_cotacao_chamado is False
        assert api_spy.recuperar_nome_moeda_chamado is False
        assert textos == [
            'Posso converter um valor em Reais para outra moeda usando a cotação atual.',
            '\tO comando é: valor para codigo_moeda. Exempo: \"100 para USD\" converte 100 reais para dólares.',
            '\tA lista de moedas que tenho acesso é:',
            '\t\tFOO: Moeda Foo',
            '\t\tBAR: Moeda Bar',
        ]

    @assert_should_raise(FormatoDesconhecido)
    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_execute_ou_raise_com_comando_invalido_deve_raise(self, api_spy: APICotacoesSpy, *_: tuple[Any]) -> None:
        io_manager_spy = IOManagerSpy()
        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        habilidade.execute_ou_raise('a para USD')

        assert io_manager_spy.iniciar_chamado is False
        assert io_manager_spy.handler_leitura_passado is None
        assert io_manager_spy.imprimir_chamado_count == 0
        assert not io_manager_spy.mensagens_passadas
        assert api_spy.lista_moedas_chamado is False
        assert api_spy.obter_cotacao_chamado is False
        assert api_spy.recuperar_nome_moeda_chamado is False

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_execute_ou_raise_com_moeda_invalida_deve_imprimir_moeda_invalida(self, api_spy: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        api_spy.excecao_para_raise = MoedaInvalida()
        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        habilidade.execute_ou_raise('150 para ABC')

        assert io_manager_spy.imprimir_chamado_count == 2
        assert io_manager_spy.mensagens_passadas == [
            'Vou buscar a cotação atual e fazer a conversão...',
            'Moeda inválida. Para obter uma lista de moedas digite ajuda.',
        ]
        assert api_spy.obter_cotacao_chamado is True
        assert api_spy.codigo_moeda_passado_obter_cotacao == 'ABC'

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_execute_ou_raise_com_falha_de_download_deve_imprimir_algo_deu_errado(self, api_spy: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        api_spy.excecao_para_raise = FalhaDownload()
        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        habilidade.execute_ou_raise('150 para usd')

        assert io_manager_spy.imprimir_chamado_count == 2
        assert io_manager_spy.mensagens_passadas == [
            'Vou buscar a cotação atual e fazer a conversão...',
            'Algo deu errado. Verifique sua conexão e tente com outra moeda.',
        ]
        assert api_spy.obter_cotacao_chamado is True
        assert api_spy.codigo_moeda_passado_obter_cotacao == 'usd'

    @replace('source.habilidades.habilidade_conversao_moedas.APICotacoes', APICotacoesSpy)
    def test_execute_ou_raise_deve_retornar_valor_convertido(self, api_spy: APICotacoesSpy) -> None:
        io_manager_spy = IOManagerSpy()
        api_spy.nome_moeda_para_retornar = 'Moeda Foo'
        api_spy.cotacao_para_retornar = 100

        habilidade = HabilidadeConversaoMoeda(TestHabilidadeConversaoMoeda.__running_loop, io_manager_spy)

        habilidade.execute_ou_raise('150 para foo')

        assert api_spy.lista_moedas_chamado is False
        assert api_spy.obter_cotacao_chamado is True
        assert api_spy.codigo_moeda_passado_obter_cotacao == 'foo'
        assert api_spy.recuperar_nome_moeda_chamado is True
        assert api_spy.codigo_moeda_passado_recuperar_nome_moeda == 'foo'
        assert io_manager_spy.imprimir_chamado_count == 2
        assert io_manager_spy.mensagens_passadas == [
            'Vou buscar a cotação atual e fazer a conversão...',
            '1.5 Moeda Foo',
        ]
