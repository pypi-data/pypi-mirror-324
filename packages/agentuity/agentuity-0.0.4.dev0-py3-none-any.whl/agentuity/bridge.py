import ctypes
import json
import os
import sys
import platform
import logging
from typing import Any, Dict
import atexit
from importlib.util import find_spec

# instrumentation imports
from agentuity.instrumentation.crewai import CrewAIInstrumentation

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# log_level = os.getenv("LOG_LEVEL", "").upper()
# if log_level != "":
#     # Convert the string to a logging level
#     numeric_level = getattr(logging, log_level, None)
#     if not isinstance(numeric_level, int):
#         raise ValueError(f"Invalid log level: {log_level}")
#     # Configure the logger
#     logging.basicConfig(level=numeric_level)

print("Agentuity bridge loaded")

class Agentuity(object):
    _instance = None

    def __new__(cls):
        """Ensures that only one instance of the class exists."""
        print("__new__ is called")
        if cls._instance is None:
            cls._instance = super(Agentuity, cls).__new__(cls)
        return cls._instance

    def init(self, lib_path: str = None):
        print("Initializing Agentuity")
        if lib_path is None:
            # Try to find the library in common locations
            system = platform.system().lower()
            arch = platform.machine().lower()
            print(f"System: {system}, Arch: {arch}")

            if arch == "aarch64":
                arch = "arm64"
            
            if system == "windows":
                lib_name = "libagentuity.dll"
            elif system == "darwin":
                lib_name = "libagentuity.dylib"
            else:
                lib_name = "libagentuity.so"
            
            # Default paths to search for the library
            search_paths = [
                os.path.dirname(os.path.abspath(__file__)),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", system, arch),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../dist", system, arch),
            ]
            
            for path in search_paths:
                full_path = os.path.join(path, lib_name)
                logger.debug(f"Searching for library in {full_path}")
                if os.path.exists(full_path):
                    lib_path = full_path
                    logger.debug(f"Found library in {full_path}")
                    break
            
            if lib_path is None:
                raise RuntimeError(f"Could not find agentuity library: {lib_name}")

        self.lib = ctypes.cdll.LoadLibrary(lib_path)
        
        # Define function prototype
        self.lib.Execute.argtypes = [
            ctypes.c_char_p,  # command
            ctypes.c_char_p,  # json_data
        ]
        self.lib.Execute.restype = ctypes.c_char_p

        module_names = {
            "crewai": "crewai"
        }
        module_instances = {
            "crewai": lambda: CrewAIInstrumentation()
        }

        modules = []

        for name in module_names:
            if self.__module_exists(module_names[name]):
                logger.info(f"Instrumenting {name}")
                instance = module_instances[name]()
                instance.instrument()
                modules.append(name)

        if len(modules) == 0:
            return

        atexit.register(self.__exit_handler)
        self.__execute(command="startup", data={"language":"python", "version": sys.version,"modules":modules})

    def __module_exists(self, module_name):
        parts = module_name.split(".")
        for i in range(1, len(parts) + 1):
            logger.debug(f"Checking if .{parts[:i]} exists")
            if find_spec(".".join(parts[:i])) is None:
                return False
        return True

    def __exit_handler(self):
        self.__execute("shutdown")

    def __execute(self, command: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        # Convert data to JSON string, use None for optional parameter
        json_data = json.dumps(data) if data is not None else None
        json_bytes = json_data.encode('utf-8') if json_data is not None else None
        command_bytes = command.encode('utf-8')
        
        # Call the Go function
        result = self.lib.Execute(command_bytes, json_bytes)
        if not result:
            raise RuntimeError("Agent execution failed")
            
        # Parse response
        response = json.loads(result.decode('utf-8'))
        if 'error' in response:
            raise RuntimeError(response['error'])

        return response['result']
    
    def version(self) -> str:
        result = self.__execute("version")
        return result['version']

    def event(self, data: Dict[str, Any]) -> None:
        self.__execute("event", data)
    
    def echo(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.__execute("echo", data)

# # Example usage
# if __name__ == "__main__":
#     agent = Agentuity()

#     version = agent.version()
#     print("Version:", version)
    
#     # Test echo command with data
#     result = agent.echo({"message": "Hello, World!"})
#     print("Echo result:", result)
    
#     # Test echo command with no data
#     result = agent.echo()
#     print("Echo with no data result:", result)

#     # Test echo command with error
#     try:
#         result = agent.echo({"error":"this is a test error message"})
#     except RuntimeError as e:
#         print("Echo with error result:", e)
