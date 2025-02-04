from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import Task
from at_common_workflow.builders.task import TaskBuilder

class WorkflowBuilder:
    def __init__(self):
        self.workflow = Workflow()
    
    def add_task(self, name: str) -> 'TaskBuilder':
        """Add a task to the workflow and return a TaskBuilder for configuring it."""
        return TaskBuilder(self, name=name)

    def build(self) -> Workflow:
        """
        Build and return the workflow.
        
        Returns:
            Workflow: The built and validated workflow
        """
        return self.workflow