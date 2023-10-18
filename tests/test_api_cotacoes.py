from asyncio import new_event_loop
from typing import Never
from unittest.mock import call, patch

from pytest import ExceptionInfo

from source.excecoes.falha_download import FalhaDownload
from source.excecoes.moeda_invalida import MoedaInvalida
from source.helpers.api_cotacoes import APICotacoes
from tests.mock.mock_resposta import MockResposta
from tests.tests_dsl import replace, assert_should_raise

class TestAPICotacoes():
    @replace('source.helpers.api_cotacoes.get', MockResposta, lambda mock_get: mock_get.assert_called_once_with('https://economia.awesomeapi.com.br/json/available/uniq'))
    def test_lista_moedas_deve_retornar_valores_da_api(self, mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 200
        mock_resposta.json_para_retornar = {'foo': 'bar'}

        moedas = running_loop.run_until_complete(APICotacoes(running_loop).lista_moedas)

        assert len(list(moedas)) == 1
        assert moedas[0] == 'foo: bar'

    @replace('source.helpers.api_cotacoes.get', MockResposta)
    def test_lista_moedas_com_brl_na_resposta_deve_remover_brl(self, mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 200
        mock_resposta.json_para_retornar = {'foo': 'bar', 'BRL': 'abc'}

        moedas = running_loop.run_until_complete(APICotacoes(running_loop).lista_moedas)

        assert len(moedas) == 1
        assert moedas[0] == 'foo: bar'

    @assert_should_raise(FalhaDownload)
    @replace('source.helpers.api_cotacoes.get', MockResposta)
    def test_lista_moedas_com_resposta_nao_ok_deve_raise_falha_download(self, _: ExceptionInfo[FalhaDownload], mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 500

        running_loop.run_until_complete(APICotacoes(running_loop).lista_moedas)

    @assert_should_raise(FalhaDownload)
    def test_lista_moedas_com_get_falhando_deve_raise_falha_download(self, _: ExceptionInfo[FalhaDownload]) -> None:
        running_loop = new_event_loop()
        def get_raise() -> Never:
            raise TimeoutError()

        with patch('source.helpers.api_cotacoes.get') as mock_get:
            mock_get.side_effect = get_raise
            running_loop.run_until_complete(APICotacoes(running_loop).lista_moedas)

    @assert_should_raise(MoedaInvalida)
    @replace('source.helpers.api_cotacoes.get', MockResposta)
    def test_obter_cotacao_com_moeda_invalida_deve_raise_moeda_invalida(self, _: ExceptionInfo[MoedaInvalida], mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 200
        mock_resposta.json_para_retornar = {}

        running_loop.run_until_complete(APICotacoes(running_loop).obter_cotacao('ABC'))

    def test_obter_cotacao_deve_retornar_valor_de_compra(self) -> None:
        running_loop = new_event_loop()
        resposta_lista_moedas = MockResposta()
        resposta_lista_moedas.status_code = 200
        resposta_lista_moedas.json_para_retornar = {'FOO': 'Moeda Foo'}
        resposta_cotacao = MockResposta()
        resposta_cotacao.status_code = 200
        resposta_cotacao.json_para_retornar = {'key': {'ask': 123}}

        with patch('source.helpers.api_cotacoes.get') as mock_get:
            mock_get.side_effect = [resposta_lista_moedas, resposta_cotacao]
            valor = running_loop.run_until_complete(APICotacoes(running_loop).obter_cotacao('foo'))

        assert valor == 123
        mock_get.assert_has_calls([
            call('https://economia.awesomeapi.com.br/json/available/uniq'),
            call('https://economia.awesomeapi.com.br/json/last/FOO-BRL'),
        ])

    @assert_should_raise(MoedaInvalida)
    @replace('source.helpers.api_cotacoes.get', MockResposta)
    def test_recuperar_nome_moeda_com_moeda_invalida_deve_raise(self, _: ExceptionInfo[MoedaInvalida], mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 200
        mock_resposta.json_para_retornar = {}

        running_loop.run_until_complete(APICotacoes(running_loop).recuperar_nome_moeda('abc'))

    @replace('source.helpers.api_cotacoes.get', MockResposta)
    def test_recuperar_nome_moeda_deve_retornar_nome(self, mock_resposta: MockResposta) -> None:
        running_loop = new_event_loop()
        mock_resposta.status_code = 200
        mock_resposta.json_para_retornar = {'FOO': 'Moeda Foo'}

        nome = running_loop.run_until_complete(APICotacoes(running_loop).recuperar_nome_moeda('foo'))

        assert nome == 'Moeda Foo'
