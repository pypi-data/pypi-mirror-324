from typing import Any, Dict
from ..types.exceptions import TaskValidationError, WorkflowValidationError

def validate_workflow(workflow: 'Workflow') -> None:
    """Validate workflow configuration and dependencies"""
    try:
        workflow._build_dependency_graph()
    except Exception as e:
        raise WorkflowValidationError(f"Workflow validation failed: {str(e)}")

def validate_task(task: 'Task', input_data: Dict[str, Any]) -> None:
    """Validate task input data against its schema"""
    try:
        task.input_model(**input_data)
    except Exception as e:
        raise TaskValidationError(f"Task '{task.name}' validation failed: {str(e)}")