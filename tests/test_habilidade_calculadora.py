from pytest import ExceptionInfo

from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.habilidades.habilidade_calculadora import HabilidadeCalculadora
from tests.spy.io_manager_spy import IOManagerSpy
from tests.tests_dsl import assert_should_raise, assert_io_manager_not_called

# pylint: disable=missing-function-docstring
class TestHabilidadeCalculadora():
    def test_textos_ajuda_deve_retornar_textos_de_ajuda(self) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeCalculadora(spy)

        textos = habilidade.textos_ajuda

        assert_io_manager_not_called(spy)
        assert textos == [
            'Consigo resolver cálculos no formato: operando_1 operador operando_2',
            '\toperando_1 e operando_2 devem ser números;',
            '\toperador deve ser: +, -, * ou /;',
            '\texemplo: -5 * 56.78'
        ]

    @assert_should_raise(FormatoDesconhecido)
    def test_execute_ou_raise_com_expressao_invalida_deve_raise(self, _: ExceptionInfo[FormatoDesconhecido]) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeCalculadora(spy)

        habilidade.execute_ou_raise('1 + a')

        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 0
        assert not spy.mensagens_passadas

    def test_execute_ou_raise_com_soma_deve_imprimir_resultado(self) -> None:
        self.__assert_expressao('-1+-10', float(-11))

    def __assert_expressao(self, expressao: str, result: float | str) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeCalculadora(spy)

        habilidade.execute_ou_raise(expressao)

        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 1
        assert spy.mensagens_passadas == [f'{result}']

    def test_execute_ou_raise_com_subtracao_deve_imprimir_resultado(self) -> None:
        self.__assert_expressao('11.5 - 1.5', float(10))

    def test_execute_ou_raise_com_multiplicacao_deve_imprimir_resultado(self) -> None:
        self.__assert_expressao('0 * 1450.59', float(0))

    def test_execute_ou_raise_com_divisao_deve_imprimir_resultado(self) -> None:
        self.__assert_expressao('150 / 2', float(75))

    def test_execute_ou_raise_com_divisao_por_zero_deve_imprimir_divisao_invalida(self) -> None:
        self.__assert_expressao('150 / 0', 'Divisão inválida.')
