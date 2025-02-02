from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import Task
from at_common_workflow.builders.task import TaskBuilder
from at_common_workflow.types.exceptions import WorkflowValidationError

class WorkflowBuilder:
    def __init__(self):
        self.workflow = Workflow()
    
    def add_task(self, task: Task) -> 'TaskBuilder':
        """Add a task to the workflow and return a TaskBuilder for configuring it."""
        return TaskBuilder(self, task)

    def _validate(self) -> None:
        """
        Validate the workflow configuration.
        Checks for cyclic dependencies and other potential issues.
        
        Raises:
            WorkflowValidationError: If there are cyclic dependencies or other validation errors
        """
        try:
            # Build the dependency graph just once for validation
            self.workflow._build_dependency_graph()
            
            # Check for cycles
            for task_node in self.workflow.tasks:
                if self.workflow.has_cycle(task_node.task.name):
                    raise WorkflowValidationError(
                        f"Cyclic dependency detected involving task: {task_node.task.name}"
                    )
        except Exception as e:
            if not isinstance(e, WorkflowValidationError):
                raise WorkflowValidationError(f"Workflow validation failed: {str(e)}")
            raise
    
    def build(self) -> Workflow:
        """
        Build and return the workflow.
        The workflow will be validated before being returned.
        
        Returns:
            Workflow: The built and validated workflow
            
        Raises:
            ValueError: If there are validation errors in the workflow
        """
        self._validate()
        # Mark the workflow as validated to avoid rebuilding the dependency graph
        self.workflow._validated = True
        return self.workflow