from typing import Any
from unittest.mock import patch, Mock

from source.io_manager import HandlerLeitura
from source.severino import Severino
from tests.mock.habilidade_mock import HabilidadeMock
from tests.spy.habilidade_sistema_spy import HabilidadeSistemaSpy
from tests.spy.io_manager_spy import IOManagerSpy
from tests.tests_dsl import replace

class TestSeverino():
    @replace('source.severino.IOManager', IOManagerSpy)
    def test_init_deve_iniciar_servicos(self, io_manager_mock: IOManagerSpy) -> None:
        Severino()

        assert io_manager_mock.iniciar_chamado is True

    @replace('source.severino.HabilidadeSistema', HabilidadeSistemaSpy)
    @replace('source.severino.IOManager', IOManagerSpy)
    def test_init_deve_imprimir_mensagem_inicial(self, habilidade_mock: HabilidadeSistemaSpy, io_manager_mock: IOManagerSpy) -> None:
        habilidade_mock.textos_para_retornar = ['foo bar']

        Severino()

        assert io_manager_mock.imprimir_chamado_count == 2
        assert io_manager_mock.mensagens_passadas == [
            'Sou o Severino, o seu faz-quase-tudo.',
            '- foo bar'
        ]

    @replace('source.severino.HabilidadeSistema', HabilidadeSistemaSpy)
    @replace('source.severino.IOManager', IOManagerSpy)
    def test_handler_leitura_recebida_quando_conhece_o_comando_deve_buscar_na_lista_de_habilidades_e_parar(self, habilidade_mock: HabilidadeSistemaSpy, io_manager_mock: IOManagerSpy) -> None:
        Severino()

        handler_leitura = self.__assert_possui_handler_leitura(io_manager_mock)
        handler_leitura('comando conhecido')

        assert habilidade_mock.execute_ou_raise_chamado is True
        assert habilidade_mock.comando_passado == 'comando conhecido'
        assert 'Não conheço esse comando.' not in io_manager_mock.mensagens_passadas

    def __assert_possui_handler_leitura(self, io_manager_mock: IOManagerSpy) -> HandlerLeitura:
        if not io_manager_mock.handler_leitura_passado:
            assert False
        return io_manager_mock.handler_leitura_passado

    @replace('source.severino.IOManager', IOManagerSpy)
    def test_handler_leitura_recebida_quando_nao_conhece_o_comando_deve_buscar_na_lista_de_habilidades_e_imprimir(self, io_manager_mock: IOManagerSpy) -> None:
        Severino()

        handler_leitura = self.__assert_possui_handler_leitura(io_manager_mock)
        handler_leitura('foo bar')

        assert io_manager_mock.imprimir_chamado_count > 0
        assert io_manager_mock.mensagens_passadas[-1] == 'Não conheço esse comando.'

    @patch('source.severino.HabilidadeSistema')
    @replace('source.severino.IOManager', IOManagerSpy)
    @replace('source.severino.HabilidadeCalculadora', HabilidadeMock)
    @replace('source.severino.HabilidadeConversaoMoeda', HabilidadeMock)
    def test_get_textos_ajuda_deve_pedir_textos_de_ajuda_para_habilidades(self, mock_construtor_habilidade_sistema: Mock, *args: tuple[Any]) -> None:
        habilidade_mock = HabilidadeSistemaSpy()
        habilidade_mock.textos_para_retornar = ['foo', 'bar']
        mock_construtor_habilidade_sistema.return_value = habilidade_mock
        Severino()
        call_args = mock_construtor_habilidade_sistema.call_args # recupera argumentos passados no __init__
        get_textos_ajuda = call_args[0][-1] # a funcao esta na ultima posicao

        result = get_textos_ajuda()

        assert result == ['foo', 'bar']
