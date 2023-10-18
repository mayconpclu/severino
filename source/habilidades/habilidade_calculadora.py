from typing import Any

from source.helpers.avaliador_regex import AvaliadorRegex
from source.excecoes.expressao_invalida import ExpressaoInvalida
from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.modelos.regex_grupo_interesse import RegexGrupoInteresse
from source.modelos.habilidade import Habilidade
from source.io_manager import IOManager

class HabilidadeCalculadora(Habilidade):
    __R = r'^([-,+]?\d+(\.\d+)?) ?([\+,\-,\*,\/]) ?([-,+]?\d+(\.\d+)?$)'
    __NE = 0
    __O = 2
    __ND = 3

    @property
    def textos_ajuda(self) -> list[str]:
        return [
            'Consigo resolver cálculos no formato: operando_1 operador operando_2',
            '\toperando_1 e operando_2 devem ser números;',
            '\toperador deve ser: +, -, * ou /;',
            '\texemplo: -5 * 56.78'
        ]

    def __init__(self, io_manager: IOManager) -> None:
        self.__io_m = io_manager
        self.__a_r = AvaliadorRegex(HabilidadeCalculadora.__R, [
            RegexGrupoInteresse(HabilidadeCalculadora.__NE, float),
            RegexGrupoInteresse(HabilidadeCalculadora.__O, str),
            RegexGrupoInteresse(HabilidadeCalculadora.__ND, float),
        ])

    def execute_ou_raise(self, comando: str) -> None:
        ne, o, nd = self.__v(comando)
        r = self.__c(ne, o, nd)
        self.__io_m.imprimir(r)

    def __v(self, s: str) -> list[Any]:
        try:
            return self.__a_r.avaliar(s)
        except ExpressaoInvalida:
            raise FormatoDesconhecido()

    def __c(self, ne: float, o: str, nd: float) -> str:
        match(o):
            case '+': return f'{ne + nd}'
            case '-': return f'{ne - nd}'
            case '*': return f'{ne * nd}'
            case '/': return self.__t_d(ne, nd)
            case _: raise FormatoDesconhecido() # nunca atingido

    def __t_d(self, ne: float, nd: float) -> str:
        try:
            return f'{ne / nd}'
        except ZeroDivisionError:
            return 'Divisão inválida.'
