from typing import Any, Callable, Optional
from unittest.mock import patch, Mock

from pytest import raises

from tests.spy.io_manager_spy import IOManagerSpy

def assert_should_raise(exception_type: type[BaseException]) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Decorator que utiliza `pytest.raise` para validar se a exceção foi lançada.\n
    O modelo `ExceptionInfo[ExceptionType]` é injetado nos `*args` da função, sendo `ExceptionType` o tipo passado no parâmetro `exception_type`.
    """
    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            with raises(exception_type) as e:
                function(*args + (e,), **kwargs)
        return wrapper
    return decorator

def replace(import_path: str, mock_type: Optional[type[object]], custom_assert: Optional[Callable[[Mock], None]] = None) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Decorator que utiliza `unittest.mock.patch` para substituir o import passado no argumento `import_path` por um objeto 
    do tipo passado no argumento `mock_type`. A instância substituta é injetada nos `*args` da função.\n
    Opcionalmente, o callback `custom_assert` pode ser utilizado para realizar validações da própria chamada do 
    import substituido.
    """
    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            with patch(import_path) as mock_creator:
                mock = mock_type() if mock_type else None
                mock_creator.return_value = mock
                function(*args + (mock,), **kwargs)
                if custom_assert:
                    custom_assert(mock_creator)
        return wrapper
    return decorator

def assert_io_manager_not_called(io_manager_spy: IOManagerSpy) -> None:
    """
    Valida que o IOManager não foi chamado.
    """
    assert io_manager_spy.iniciar_chamado is False
    assert io_manager_spy.handler_leitura_passado is None
    assert io_manager_spy.imprimir_chamado_count == 0
    assert not io_manager_spy.mensagens_passadas
