from agentuity.bridge import Agentuity
from typing import Any, Dict

print("Agentuity __init__ starting")

instance = Agentuity()

print("Agentuity __init__ after instance")

def init(lib_path: str = None):
    return instance.init(lib_path)

def echo(data: Dict[str, Any] = None) -> Dict[str, Any]:
    return instance.echo(data)

def event(data: Dict[str, Any]) -> None:
    return instance.event(data)

def version() -> str:
    return instance.version()

__version__ = "0.0.8-dev"

print("Agentuity __init__ loaded")