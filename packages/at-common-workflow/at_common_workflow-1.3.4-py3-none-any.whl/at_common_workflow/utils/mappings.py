from typing import Any, Optional, Union
from pydantic import BaseModel

from at_common_workflow.core.context import Context

class BaseMapping:
    """Base class for all mapping types."""
    
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class ArgumentMapping(BaseMapping):
    """Maps context values or constants to task arguments."""
    
    def __init__(self, value: Union[str, Any]):
        self.value = value
        self.is_context_ref = isinstance(value, str) and value.startswith("$")
    
    def resolve(self, context: Context) -> Any:
        """Resolve the mapping value from context if it's a reference."""
        if self.is_context_ref:
            return context.get(self.value[1:])
        return self.value

class ResultMapping(BaseMapping):
    """Maps task results to context keys."""
    
    def __init__(self, context_key: str, result_path: Optional[str] = None):
        self.context_key = context_key
        self.result_path = result_path
    
    def store(self, context: Context, result: BaseModel) -> None:
        """Store the task result in the context."""
        value = getattr(result, self.result_path) if self.result_path else result
        context.set(self.context_key, value)