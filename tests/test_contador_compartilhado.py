from threading import Thread

from source.helpers.contador_compartilhado import ContadorCompartilhado

# pylint: disable=missing-function-docstring
class TestContadorCompartilhado():
    def test_recuperar_deve_retornar_valor(self) -> None:
        contador = ContadorCompartilhado(3)

        valor = contador.recuperar()

        assert valor == 3

    def test_incrementar_deve_incrementar_valor_em_um(self) -> None:
        contador = ContadorCompartilhado(5)

        contador.incrementar()

        assert contador.recuperar() == 6

    def test_recuperar_e_incrementar_deve_retornar_valor_atual_e_incrementar_contador_em_um(self) -> None:
        contador = ContadorCompartilhado(11)

        valor = contador.recuperar_e_incrementar()

        assert valor == 11
        assert contador.recuperar() == 12

    def test_incrementar_de_duas_threads_deve_ter_resultado_incrementado_em_dois(self) -> None:
        contador = ContadorCompartilhado(0)

        thread_a = Thread(target=contador.incrementar)
        thread_b = Thread(target=contador.incrementar)
        thread_a.start()
        thread_b.start()

        assert contador.recuperar() == 2
