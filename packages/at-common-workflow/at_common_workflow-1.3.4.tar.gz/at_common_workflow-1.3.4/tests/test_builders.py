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

async def execute_add(input: AddInputModel) -> AddOutputModel:
    return AddOutputModel(result=input.a + input.b)

@pytest.mark.asyncio
async def test_task_builder_initialization():
    workflow = (WorkflowBuilder()
        .add_task("add_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_func=execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .store_result("add_task_result", "result")
        .build()
    )

    # Assert that the workflow is not None
    assert workflow is not None

    # Assert that the task was added to the workflow
    assert len(workflow.tasks) == 1  # Assuming only one task is added

    # Assert that the task's name is correct
    task_node = workflow.tasks[0]
    assert task_node.task.name == "add_task"

    # Assert that the input model is set correctly
    assert task_node.task.input_model is AddInputModel

    # Assert that the output model is set correctly
    assert task_node.task.output_model is AddOutputModel

    # Assert that the constant arguments are mapped correctly
    assert task_node.argument_mappings["a"].value == 5
    assert task_node.argument_mappings["b"].value == 3

    # Assert that the result mapping is set correctly
    assert task_node.result_mapping.context_key == "add_task_result"

@pytest.mark.asyncio
async def test_task_builder_with_description():
    workflow = (WorkflowBuilder()
        .add_task("add_task")
            .with_description("Adds two numbers")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .store_result("result")
        .build()
    )
    
    assert workflow.tasks[0].task.description == "Adds two numbers"

@pytest.mark.asyncio
async def test_task_builder_with_context_arg():
    workflow = (WorkflowBuilder()
        .add_task("first_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .store_result("first_result", "result")
        .add_task("second_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "first_result")
            .with_constant_arg("b", 2)
        .store_result("final_result", "result")
        .build()
    )
    
    assert len(workflow.tasks) == 2
    second_task = workflow.tasks[1]
    assert second_task.argument_mappings["a"].value == "$first_result"
    assert second_task.argument_mappings["b"].value == 2

@pytest.mark.asyncio
async def test_task_builder_invalid_input_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="input_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .add_task("invalid_task")
                .with_input_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_missing_required_components():
    # Missing input model
    with pytest.raises(ValueError, match="Input model must be defined"):
        (WorkflowBuilder()
            .add_task("incomplete_task")
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .store_result("result")
        )
    
    # Missing execute function
    with pytest.raises(ValueError, match="Execute function must be defined"):
        (WorkflowBuilder()
            .add_task("incomplete_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .store_result("result")
        )

@pytest.mark.asyncio
async def test_task_builder_invalid_constant_arg():
    with pytest.raises(ValueError, match="Constant argument .* looks like a context reference"):
        (WorkflowBuilder()
            .add_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", "$invalid_ref")
        )

@pytest.mark.asyncio
async def test_multiple_tasks_workflow():
    # Create a more complex workflow with multiple tasks
    workflow = (WorkflowBuilder()
        .add_task("task1")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .store_result("result1", "result")
        .add_task("task2")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "result1")
            .with_constant_arg("b", 2)
        .store_result("final_result", "result")
        .build()
    )
    
    assert len(workflow.tasks) == 2
    
    # Verify first task
    task1 = workflow.tasks[0]
    assert task1.task.name == "task1"
    assert task1.argument_mappings["a"].value == 5
    assert task1.argument_mappings["b"].value == 3
    assert task1.result_mapping.context_key == "result1"
    assert task1.result_mapping.result_path == "result"
    
    # Verify second task
    task2 = workflow.tasks[1]
    assert task2.task.name == "task2"
    assert task2.argument_mappings["a"].value == "$result1"
    assert task2.argument_mappings["b"].value == 2
    assert task2.result_mapping.context_key == "final_result"
    assert task2.result_mapping.result_path == "result"

@pytest.mark.asyncio
async def test_task_builder_invalid_output_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="output_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .add_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_chaining():
    # Test that all builder methods return self for proper chaining
    builder = WorkflowBuilder().add_task("chain_task")
    
    # Test each method returns the builder instance
    assert builder.with_description("test") is builder
    assert builder.with_input_model(AddInputModel) is builder
    assert builder.with_output_model(AddOutputModel) is builder
    assert builder.with_execute_func(execute_add) is builder
    assert builder.with_constant_arg("a", 1) is builder
    assert builder.with_context_arg("b", "some_key") is builder

@pytest.mark.asyncio
async def test_task_builder_result_paths():
    # Create a more complex output model for testing result paths
    class ComplexOutputModel(BaseModel):
        value: int
        nested: dict
        items: list

    async def complex_execute(input: AddInputModel) -> ComplexOutputModel:
        return ComplexOutputModel(
            value=input.a + input.b,
            nested={"result": input.a * input.b},
            items=[input.a, input.b]
        )

    workflow = (WorkflowBuilder()
        .add_task("complex_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .store_result("result1", "value")  # Store just the value field
        .add_task("nested_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 2)
            .with_constant_arg("b", 4)
        .store_result("result2", "nested.result")  # Store nested field
        .build()
    )
    
    assert len(workflow.tasks) == 2
    assert workflow.tasks[0].result_mapping.result_path == "value"
    assert workflow.tasks[1].result_mapping.result_path == "nested.result"

@pytest.mark.asyncio
async def test_task_builder_duplicate_task_names():
    workflow_builder = WorkflowBuilder()
    
    # Add first task
    workflow_builder.add_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 1) \
        .with_constant_arg("b", 2) \
        .store_result("result1")
    
    # Add second task with same name
    workflow_builder.add_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 3) \
        .with_constant_arg("b", 4) \
        .store_result("result2")
    
    # Build should succeed as duplicate names are allowed
    workflow = workflow_builder.build()
    assert len(workflow.tasks) == 2
    assert workflow.tasks[0].task.name == "same_name"
    assert workflow.tasks[1].task.name == "same_name"