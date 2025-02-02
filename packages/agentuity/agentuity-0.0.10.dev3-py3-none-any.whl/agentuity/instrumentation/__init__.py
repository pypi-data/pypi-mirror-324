from abc import ABC, abstractmethod
from typing import Any
from logging import getLogger
from wrapt import wrap_function_wrapper

logger = getLogger(__name__)

class BaseInstrumentation(ABC):
	_instance = None
	_is_instrumented_by_agentuity = False

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = object.__new__(cls)
		print(f"BaseInstrumentation __new__ returning {cls._instance}")
		return cls._instance
	
	@property
	def is_instrumented_by_agentuity(self):
		return self._is_instrumented_by_agentuity
	
	@abstractmethod
	def _instrument(self, **kwargs: Any):
		pass

	def _uninstrument(self, **kwargs: Any):
		pass

	def instrument(self, **kwargs: Any):
		"""Instrument the library"""
		if self._is_instrumented_by_agentuity:
			logger.warning("Attempting to instrument while already instrumented")
			return None
		print(f"Instrumenting {self.__class__.__name__}")
		result = self._instrument(**kwargs)
		print(f"Instrumented {self.__class__.__name__}")
		self._is_instrumented_by_agentuity = True
		return result

	def uninstrument(self, **kwargs: Any):
		"""Uninstrument	the library"""
		if self._is_instrumented_by_agentuity:
			result = self._uninstrument(**kwargs)
			self._is_instrumented_by_agentuity = False
			return result

		logger.warning("Attempting to uninstrument while already uninstrumented")

		return None

	def _wrap(self, module, fn, before = None, after = None):
		print(f"Wrapping {module}.{fn}")
		def wrapper(wrapped, instance, args, kwargs):
			instance_class = instance.__class__.__name__
			if before is not None:
				before(kwargs)
			response = wrapped(*args, **kwargs)
			if after is not None:
				after(kwargs, response)
			return response
		wrap_function_wrapper(module, fn, wrapper)
		print(f"Wrapped {module}.{fn}")
		return wrapper


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False

__all__ = ["BaseInstrumentor", "is_jsonable"]