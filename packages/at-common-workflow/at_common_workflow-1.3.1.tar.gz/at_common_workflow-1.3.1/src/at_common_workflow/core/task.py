from typing import TypeVar, Generic, Type, Any
from pydantic import BaseModel

InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)

class Task(Generic[InputType, OutputType]):
    """
    Base class for all tasks in the workflow.
    Users should implement:
    1. input_model: Pydantic model defining expected input parameters
    2. output_model: Pydantic model defining the task's output
    3. execute(): The actual task logic
    """
    input_model: Type[InputType]
    output_model: Type[OutputType]
    
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Task name must be a string")
        if not name.strip():
            raise ValueError("Task name cannot be empty")
            
        self.name = name
        self._validate_models()
        
    def _validate_models(self) -> None:
        """Validate that input and output models are properly defined."""
        if not hasattr(self, "input_model") or not hasattr(self, "output_model"):
            raise ValueError(
                f"Task {self.name} must define both input_model and output_model"
            )
        
        if not (isinstance(self.input_model, type) and issubclass(self.input_model, BaseModel)):
            raise TypeError(f"input_model must be a Pydantic model class")
        if not (isinstance(self.output_model, type) and issubclass(self.output_model, BaseModel)):
            raise TypeError(f"output_model must be a Pydantic model class")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
    
    async def _execute(self, input: InputType) -> OutputType:
        """
        Execute the task with validated input data.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Task subclasses must implement execute method")
    
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
        output = await self._execute(input)
        return self._validate_output(output)