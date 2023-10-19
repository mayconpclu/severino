from json import JSONDecoder
from typing import Any, Callable

from requests import Response

class MockResposta(Response):
    def __init__(self) -> None:
        super().__init__()
        self.json_para_retornar: Any = {}

    # pylint: disable=line-too-long,unused-argument,too-many-arguments
    def json(self, *, cls: type[JSONDecoder] | None = None, object_hook: Callable[[dict[Any, Any]], Any] | None = None, parse_float: Callable[[str], Any] | None = None, parse_int: Callable[[str], Any] | None = None, parse_constant: Callable[[str], Any] | None = None, object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None, **kwds: Any) -> Any:
        return self.json_para_retornar
