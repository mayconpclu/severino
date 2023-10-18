from pytest import ExceptionInfo

from tests.tests_dsl import assert_should_raise
from source.excecoes.expressao_invalida import ExpressaoInvalida
from source.helpers.avaliador_regex import AvaliadorRegex
from source.modelos.regex_grupo_interesse import RegexGrupoInteresse

class TestAvaliadorRegex():
    __REGEX_INT_CHAR_INT = r'^(\d)([A-Za-z])(\d)$'

    @assert_should_raise(ExpressaoInvalida)
    def test_avaliar_com_expressao_invalida_deve_raise(self, _: ExceptionInfo[ExpressaoInvalida]) -> None:
        avaliador = AvaliadorRegex(TestAvaliadorRegex.__REGEX_INT_CHAR_INT, [])

        avaliador.avaliar('123')

    def test_avaliar_com_expressao_valida_deve_retornar_valores(self) -> None:
        index_grupo_int_antes = 0
        index_grupo_char = 1
        index_grupo_int_depois = 2
        avaliador = AvaliadorRegex(TestAvaliadorRegex.__REGEX_INT_CHAR_INT, [
            RegexGrupoInteresse(index_grupo_int_antes, int),
            RegexGrupoInteresse(index_grupo_char, str),
            RegexGrupoInteresse(index_grupo_int_depois, int),
        ])

        int_antes, char, int_depois = avaliador.avaliar('1a2')

        assert int_antes == 1
        assert char == 'a'
        assert int_depois == 2

    @assert_should_raise(ExpressaoInvalida)
    def test_avaliar_com_index_de_grupo_invalido_deve_raise(self, _: ExceptionInfo[ExpressaoInvalida]) -> None:
        avaliador = AvaliadorRegex(TestAvaliadorRegex.__REGEX_INT_CHAR_INT, [
            RegexGrupoInteresse(999, int),
        ])

        avaliador.avaliar('1a2')
