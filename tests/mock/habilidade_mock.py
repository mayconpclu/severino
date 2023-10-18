from source.modelos.habilidade import Habilidade

class HabilidadeMock(Habilidade):
    @property
    def textos_ajuda(self) -> list[str]:
        return []

    def execute_ou_raise(self, comando: str) -> None:
        raise NotImplementedError()
