from unittest.mock import Mock, patch

from pytest import CaptureFixture

from source.io_manager import IOManager

class TestIOManager():
    def test_iniciar_deve_imprimir_numero_da_linha(self, capsys: CaptureFixture[str]) -> None:
        io_manager = IOManager()

        io_manager.iniciar(lambda _: None)
        stdout, erro = capsys.readouterr()

        assert stdout == '0001 |\t'
        assert erro == ''

    def test_leitura_deve_chamar_handler_leitura(self) -> None:
        io_manager = IOManager()
        handler_leitura_mock = Mock()
        texto_digitado = 'foo bar'

        with patch('builtins.input', lambda: texto_digitado), patch('builtins.print'):
            io_manager.iniciar(handler_leitura_mock)

        handler_leitura_mock.assert_called_with(texto_digitado)

    def test_imprimir_deve_imprimir_mensagem_em_ciano_e_numero_da_linha(self, capsys: CaptureFixture[str]) -> None:
        io_manager = IOManager()
        io_manager.iniciar(lambda _: None)
        mensagem = 'foo bar'

        io_manager.imprimir(mensagem)
        stdout, erro = capsys.readouterr()

        assert stdout == f'0001 |\t{IOManager.COR_CIANO}{mensagem}{IOManager.FIM_COR}\n0002 |\t'
        assert erro == ''
