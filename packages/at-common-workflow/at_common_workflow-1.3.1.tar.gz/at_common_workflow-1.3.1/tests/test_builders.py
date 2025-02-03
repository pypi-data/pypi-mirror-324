import pytest
from at_common_workflow.builders.workflow import WorkflowBuilder
from at_common_workflow.builders.task import TaskBuilder
from at_common_workflow.core.task import Task
from at_common_workflow.types.exceptions import WorkflowValidationError
from pydantic import BaseModel

class AddInputModel(BaseModel):
    a: int
    b: int

class AddOutputModel(BaseModel):
    result: int

class AddTask(Task[AddInputModel, AddOutputModel]):
    input_model = AddInputModel
    output_model = AddOutputModel
    
    async def _execute(self, input: AddInputModel) -> AddOutputModel:
        return AddOutputModel(result=input.a + input.b)

@pytest.mark.asyncio
async def test_task_builder_initialization():
    workflow_builder = WorkflowBuilder()
    task = AddTask("add_task")
    task_builder = TaskBuilder(workflow_builder, task)
    
    assert task_builder.workflow_builder == workflow_builder
    assert task_builder.task == task

def test_with_constant_arg():
    workflow_builder = WorkflowBuilder()
    task = AddTask("add_task")
    task_builder = TaskBuilder(workflow_builder, task)
    
    task_builder.with_constant_arg("arg1", 10)
    assert "arg1" in task_builder.argument_mappings

    with pytest.raises(ValueError):
        task_builder.with_constant_arg("arg2", "$context_key")

def test_with_context_arg():
    workflow_builder = WorkflowBuilder()
    task = AddTask("add_task")
    task_builder = TaskBuilder(workflow_builder, task)
    
    task_builder.with_context_arg("arg1", "context_key")
    assert "arg1" in task_builder.argument_mappings
    assert task_builder.argument_mappings["arg1"].value == "$context_key"

@pytest.mark.asyncio
async def test_workflow_builder_add_task():
    workflow_builder = WorkflowBuilder()
    task = AddTask("add_task")
    task_builder = workflow_builder.add_task(task)
    
    assert isinstance(task_builder, TaskBuilder)

@pytest.mark.asyncio
async def test_workflow_builder_build():
    workflow_builder = WorkflowBuilder()
    task = AddTask("add_task")
    workflow_builder.add_task(task)
    
    workflow = workflow_builder.build()
    assert workflow is not None 