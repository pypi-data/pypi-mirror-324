from typing import Any, Optional, TYPE_CHECKING
from at_common_workflow.core.task import Task
from at_common_workflow.utils.mappings import ArgumentMapping

if TYPE_CHECKING:
    from at_common_workflow.builders.workflow import WorkflowBuilder

class TaskBuilder:
    def __init__(self, workflow_builder: 'WorkflowBuilder', task: Task):
        self.workflow_builder = workflow_builder
        self.task = task
        self.argument_mappings = {}
        
    def with_constant_arg(self, arg_name: str, value: Any) -> 'TaskBuilder':
        """Map an argument to a constant value"""
        if isinstance(value, str) and value.startswith('$'):
            raise ValueError(
                "Direct values cannot start with '$'. "
                "Use with_context_arg() for context references."
            )
        self.argument_mappings[arg_name] = ArgumentMapping(value)
        return self
    
    def with_context_arg(self, arg_name: str, context_key: str) -> 'TaskBuilder':
        """Map an argument to a context value"""
        self.argument_mappings[arg_name] = ArgumentMapping(f"${context_key}")
        return self
        
    def store_result(self, context_key: str, result_path: Optional[str] = None) -> 'WorkflowBuilder':
        """Store the task result in the context"""
        result_mapping = (context_key, result_path) if result_path else context_key
        self.workflow_builder.workflow.add_task(self.task, self.argument_mappings, result_mapping)
        return self.workflow_builder