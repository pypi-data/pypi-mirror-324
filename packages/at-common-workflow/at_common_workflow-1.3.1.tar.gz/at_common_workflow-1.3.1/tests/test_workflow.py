import pytest
from at_common_workflow.core.workflow import Workflow, TaskStatus
from at_common_workflow.core.task import Task
from pydantic import BaseModel
import asyncio

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
async def test_workflow_execution():
    workflow = Workflow()
    task = AddTask("add_numbers")
    
    # Test adding task
    workflow.add_task(
        task=task,
        argument_mappings={"a": 5, "b": 3},
        result_mapping="result"
    )
    
    # Test execution
    await workflow.execute()
    assert workflow.context.get("result").result == 8

@pytest.mark.asyncio
async def test_workflow_dependencies():
    workflow = Workflow()
    task1 = AddTask("task1")
    task2 = AddTask("task2")
    
    workflow.add_task(
        task=task1,
        argument_mappings={"a": 5, "b": 3},
        result_mapping=("result1", "result")  
    )
    
    workflow.add_task(
        task=task2,
        argument_mappings={"a": "$result1", "b": 2},  
        result_mapping="result2"
    )

    await workflow.execute()
    
    assert workflow.context.get("result2").result == 10

@pytest.mark.asyncio
async def test_workflow_progress():
    workflow = Workflow()
    task = AddTask("add_numbers")
    workflow.add_task(task, {"a": 1, "b": 2}, "result")
    
    events = []
    workflow.on_task_start = lambda name: events.append(f"start_{name}")
    workflow.on_task_complete = lambda name: events.append(f"complete_{name}")
    
    await workflow.execute()
    assert events == ["start_add_numbers", "complete_add_numbers"]

@pytest.mark.asyncio
async def test_workflow_cyclic_dependencies():
    workflow = Workflow()
    task1 = AddTask("task1")
    task2 = AddTask("task2")
    
    workflow.add_task(
        task=task2,
        argument_mappings={"a": "$result1", "b": 2},
        result_mapping="result2"
    )
    
    workflow.add_task(
        task=task1,
        argument_mappings={"a": "$result2", "b": 1},
        result_mapping="result1"
    )
    
    # The validation should catch the cycle during execute()
    with pytest.raises(ValueError, match="Cyclic dependencies detected in workflow"):
        await workflow.execute()

@pytest.mark.asyncio
async def test_workflow_duplicate_result_keys():
    workflow = Workflow()
    task1 = AddTask("task1")
    task2 = AddTask("task2")
    
    workflow.add_task(
        task=task1,
        argument_mappings={"a": 1, "b": 2},
        result_mapping="same_key"
    )
    
    workflow.add_task(
        task=task2,
        argument_mappings={"a": 3, "b": 4},
        result_mapping="same_key"
    )
    
    with pytest.raises(ValueError, match="Multiple tasks trying to write to context key"):
        await workflow.execute()

@pytest.mark.asyncio
async def test_workflow_missing_dependency():
    workflow = Workflow()
    task = AddTask("task1")
    
    workflow.add_task(
        task=task,
        argument_mappings={"a": "$nonexistent", "b": 1},
        result_mapping="result"
    )
    
    with pytest.raises(RuntimeError, match="Unable to make progress"):
        await workflow.execute()

@pytest.mark.asyncio
async def test_workflow_parallel_execution():
    class DelayedAddTask(AddTask):
        async def _execute(self, input: AddInputModel) -> AddOutputModel:
            await asyncio.sleep(0.1)  # Add a small delay
            return AddOutputModel(result=input.a + input.b)
    
    workflow = Workflow()
    task1 = DelayedAddTask("task1")
    task2 = DelayedAddTask("task2")
    task3 = DelayedAddTask("task3")
    
    # task1 and task2 can run in parallel, task3 depends on both
    workflow.add_task(
        task=task1,
        argument_mappings={"a": 1, "b": 2},
        result_mapping=("result1", "result")
    )
    
    workflow.add_task(
        task=task2,
        argument_mappings={"a": 3, "b": 4},
        result_mapping=("result2", "result")
    )
    
    workflow.add_task(
        task=task3,
        argument_mappings={"a": "$result1", "b": "$result2"},
        result_mapping="result3"
    )
    
    # Track execution order
    execution_order = []
    workflow.on_task_start = lambda name: execution_order.append(f"start_{name}")
    workflow.on_task_complete = lambda name: execution_order.append(f"complete_{name}")
    
    await workflow.execute()
    
    # Verify results
    assert workflow.context.get("result3").result == 10  # (1+2) + (3+4)
    
    # Verify parallel execution
    start1_idx = execution_order.index("start_task1")
    start2_idx = execution_order.index("start_task2")
    complete1_idx = execution_order.index("complete_task1")
    complete2_idx = execution_order.index("complete_task2")
    start3_idx = execution_order.index("start_task3")
    
    # task1 and task2 should start before either completes
    assert min(complete1_idx, complete2_idx) > max(start1_idx, start2_idx)
    # task3 should start after both task1 and task2 complete
    assert start3_idx > max(complete1_idx, complete2_idx)

@pytest.mark.asyncio
async def test_workflow_error_handling():
    class ErrorTask(Task[AddInputModel, AddOutputModel]):
        input_model = AddInputModel
        output_model = AddOutputModel
        
        async def _execute(self, input: AddInputModel) -> AddOutputModel:
            raise ValueError("Task failed")
    
    workflow = Workflow()
    task = ErrorTask("error_task")
    
    workflow.add_task(
        task=task,
        argument_mappings={"a": 1, "b": 2},
        result_mapping="result"
    )
    
    # Track error callback
    error_events = []
    workflow.on_task_error = lambda name, e: error_events.append((name, str(e)))
    
    with pytest.raises(RuntimeError, match="Workflow execution failed"):
        await workflow.execute()
    
    assert len(error_events) == 1
    assert error_events[0][0] == "error_task"
    assert "Task failed" in error_events[0][1]
    assert workflow.progress.task_statuses["error_task"] == TaskStatus.FAILED

@pytest.mark.asyncio
async def test_workflow_result_path_mapping():
    workflow = Workflow()
    task1 = AddTask("task1")
    task2 = AddTask("task2")
    
    # Store just the result value from task1
    workflow.add_task(
        task=task1,
        argument_mappings={"a": 5, "b": 3},
        result_mapping=("output1", "result")
    )
    
    # Use the extracted result value
    workflow.add_task(
        task=task2,
        argument_mappings={"a": "$output1", "b": 2},
        result_mapping=("output2", "result")
    )
    
    await workflow.execute()
    
    # Check both raw value and full model access
    assert workflow.context.get("output1") == 8  # Direct value
    assert workflow.context.get("output2") == 10  # Direct value

@pytest.mark.asyncio
async def test_workflow_missing_context_reference():
    workflow = Workflow()
    task1 = AddTask("task1")
    
    # task1 depends on result2 which doesn't exist yet
    workflow.add_task(
        task=task1,
        argument_mappings={"a": "$result2", "b": 1},
        result_mapping="result1"
    )

    # This should fail during validation since result2 is referenced before it's created
    with pytest.raises(ValueError, match="References undefined context key"):
        await workflow.execute()