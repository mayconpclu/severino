from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
import os

from tests.tests_dsl import replace

class TestMain():
    # a def __init__ deve retornar None
    @replace('source.severino.Severino.__init__', None, lambda init_mock: init_mock.assert_called_once())
    def test_main_deve_iniciar_severino(self, _: None) -> None:
        diretorio_atual = os.path.realpath(os.path.curdir)

        # o modulo sera carregado manualmente para simular uma chamada do terminal
        # referencia: https://stackoverflow.com/a/49012866/7653600
        nome = '__main__'
        spec = spec_from_loader(nome, SourceFileLoader(nome, f'{diretorio_atual}/source/main.py'))
        assert spec is not None
        assert spec.loader is not None
        modulo = module_from_spec(spec)
        spec.loader.exec_module(modulo)
