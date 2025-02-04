from typing import TypeVar, Generic, Type, Any, Callable
from pydantic import BaseModel
from inspect import signature

InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)

class Task(Generic[InputType, OutputType]):
    def __init__(self, name: str, description: str | None, input_model: Type[InputType], output_model: Type[OutputType], execute_func: Callable[[InputType], OutputType]):
        if not isinstance(name, str):
            raise TypeError("Task name must be a string")
        if not name.strip():
            raise ValueError("Task name cannot be empty")

        self.name = name
        self.description = description
        self.input_model = input_model
        self.output_model = output_model
        self.execute_func = execute_func
        self._validate()
        
    def _validate(self) -> None:
        """Validate that input and output models are properly defined."""
        if not hasattr(self, "input_model") or not hasattr(self, "output_model"):
            raise ValueError(
                f"Task {self.name} must define both input_model and output_model"
            )
        if not (isinstance(self.input_model, type) and issubclass(self.input_model, BaseModel)):
            raise TypeError(f"input_model must be a Pydantic model class")
        if not (isinstance(self.output_model, type) and issubclass(self.output_model, BaseModel)):
            raise TypeError(f"output_model must be a Pydantic model class")
        if not callable(self.execute_func):
            raise TypeError("execute_func must be callable")
        sig = signature(self.execute_func)
        if len(sig.parameters) != 1 or list(sig.parameters)[0] != 'input':
            raise TypeError("execute_func must take exactly one parameter named 'input'")
        if sig.return_annotation != self.output_model:
            raise TypeError("execute_func must return an instance of output_model")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})(description={self.description!r}) {self.input_model.__name__} -> {self.output_model.__name__}"
    
    def _validate_input(self, **kwargs) -> InputType:
        """Validate input arguments against input_model."""
        return self.input_model(**kwargs)
    
    def _validate_output(self, output: Any) -> OutputType:
        """Validate output against output_model."""
        if isinstance(output, self.output_model):
            return output
        return self.output_model(**output)
    
    async def __call__(self, **kwargs) -> OutputType:
        """
        Allow tasks to be called directly for testing/debugging.
        Validates both input and output.
        """
        input = self._validate_input(**kwargs)
        output = await self.execute_func(input)
        return self._validate_output(output)