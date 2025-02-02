from agentuity.bridge import Agentuity
from typing import Any, Dict

instance = Agentuity()

def init(lib_path: str = None):
    return instance.init(lib_path)

def echo(data: Dict[str, Any] = None) -> Dict[str, Any]:
    return instance.echo(data)

def event(data: Dict[str, Any]) -> None:
    return instance.event(data)

def version() -> str:
    return instance.version()

__version__ = "0.0.3-dev"
