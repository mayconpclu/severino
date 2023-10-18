from pytest import ExceptionInfo

from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.habilidades.habilidade_sistema import HabilidadeSistema
from tests.spy.io_manager_spy import IOManagerSpy
from tests.tests_dsl import assert_should_raise

class TestHabilidadeSistema():
    def test_textos_ajuda_deve_retornar_textos_de_ajuda(self) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeSistema(spy, lambda: [])

        textos = habilidade.textos_ajuda

        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 0
        assert not spy.mensagens_passadas
        assert textos == [
            'Digite ajuda para ver o que eu posso fazer.',
            'Digite sair para encerrar.',
        ]

    @assert_should_raise(FormatoDesconhecido)
    def test_execute_ou_raise_com_comando_desconhecido_deve_raise_formato_desconhecido(self, _: ExceptionInfo[FormatoDesconhecido]) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeSistema(spy, lambda: [])

        habilidade.execute_ou_raise('foo bar')

        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 0
        assert not spy.mensagens_passadas

    @assert_should_raise(SystemExit)
    def test_execute_ou_raise_com_comando_sair_deve_encerrar_programa(self, exception: ExceptionInfo[SystemExit]) -> None:
        spy = IOManagerSpy()
        habilidade = HabilidadeSistema(spy, lambda: [])

        habilidade.execute_ou_raise('sair')

        assert exception.value.code == 0
        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 1
        assert len(spy.mensagens_passadas) == 1
        assert spy.mensagens_passadas[0] == 'Até mais!'

    def test_execute_ou_raise_com_comando_ajuda_deve_imprimir_mensagens_recebidas_no_init_formatadas(self) -> None:
        spy = IOManagerSpy()
        mensages = ['a', 'b']
        habilidade = HabilidadeSistema(spy, lambda: mensages)

        habilidade.execute_ou_raise('ajuda')

        assert spy.iniciar_chamado is False
        assert spy.handler_leitura_passado is None
        assert spy.imprimir_chamado_count == 2
        assert len(spy.mensagens_passadas) == len(mensages)
        assert spy.mensagens_passadas[0] == '- a'
        assert spy.mensagens_passadas[1] == '- b'
