import pytest
from pydantic import BaseModel
from at_common_workflow.core.task import Task

class _SampleInputModel(BaseModel):
    value: int
    name: str

class _SampleOutputModel(BaseModel):
    result: str

class _SampleTask(Task[_SampleInputModel, _SampleOutputModel]):
    input_model = _SampleInputModel
    output_model = _SampleOutputModel
    
    async def _execute(self, input: _SampleInputModel) -> _SampleOutputModel:
        return _SampleOutputModel(result=f"{input.name}: {input.value}")

@pytest.mark.asyncio
async def test_task_initialization():
    # Test valid task creation
    task = _SampleTask("test_task")
    assert task.name == "test_task"
    
    # Test invalid task names
    with pytest.raises(TypeError):
        _SampleTask(123)
    with pytest.raises(ValueError):
        _SampleTask("")

@pytest.mark.asyncio
async def test_task_execution():
    task = _SampleTask("test_task")
    result = await task(value=42, name="test")
    assert isinstance(result, _SampleOutputModel)
    assert result.result == "test: 42"

@pytest.mark.asyncio
async def test_task_input_validation():
    task = _SampleTask("test_task")
    with pytest.raises(ValueError):
        await task(value="not_an_int", name="test")
    with pytest.raises(ValueError):
        await task(value=42)  # missing required field 'name'