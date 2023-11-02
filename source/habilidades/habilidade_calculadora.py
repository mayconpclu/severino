from typing import Any

from source.helpers.avaliador_regex import AvaliadorRegex
from source.excecoes.expressao_invalida import ExpressaoInvalida
from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.modelos.regex_grupo_interesse import RegexGrupoInteresse
from source.modelos.habilidade import Habilidade
from source.io_manager import IOManager

class HabilidadeCalculadora(Habilidade):
    __REGEX_ACEITACAO = r'^([-,+]?\d+(\.\d+)?) ?([\+,\-,\*,\/]) ?([-,+]?\d+(\.\d+)?$)'
    __INDEX_NUMERAL_A_ESQUERDA = 0
    __INDEX_OPERADOR = 2
    __INDEX_NUMERAL_A_DIREITA = 3

    @property
    def textos_ajuda(self) -> list[str]:
        return [
            'Consigo resolver cálculos no formato: operando_1 operador operando_2',
            '\toperando_1 e operando_2 devem ser números;',
            '\toperador deve ser: +, -, * ou /;',
            '\texemplo: -5 * 56.78'
        ]

    def __init__(self, io_manager: IOManager) -> None:
        self.__io_manager = io_manager
        self.__avaliador_regex = AvaliadorRegex(HabilidadeCalculadora.REGEX_ACEITACAO, [
            RegexGrupoInteresse(HabilidadeCalculadora.__INDEX_NUMERAL_A_ESQUERDA, float),
            RegexGrupoInteresse(HabilidadeCalculadora.__INDEX_OPERADOR, str),
            RegexGrupoInteresse(HabilidadeCalculadora.__INDEX_NUMERAL_A_DIREITA, float),
        ])

    def execute_ou_raise(self, comando: str) -> None:
        numero_esquerda, o, nd = self.__v(comando)
        r = self.__calcular(numero_esquerda, o, nd)
        self.__io_manager.imprimir(r)

    def __v(self, s: str) -> list[Any]:
        try:
            return self.__avaliador_regex.avaliar(s)
        except ExpressaoInvalida:
            raise FormatoDesconhecido()

    def __calcular(self, numero_esquerda: float, o: str, nd: float) -> str:
        match(o):
            case '+': return f'{numero_esquerda + nd}'
            case '-': return f'{numero_esquerda - nd}'
            case '*': return f'{numero_esquerda * nd}'
            case '/': return self.__divisao(numero_esquerda, nd)
            case _: raise FormatoDesconhecido() # nunca atingido

    def __divisao(self, numero_esquerda: float, nd: float) -> str:
        try:
            return f'{numero_esquerda / nd}'
        except ZeroDivisionError:
            return 'Divisão inválida.'
