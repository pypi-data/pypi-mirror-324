# At Common Workflow

## Description
At Common Workflow is a workflow management system that allows users to define and execute tasks in a directed acyclic graph (DAG) structure. It supports parallel execution and provides a context manager for managing task inputs and outputs.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd at-common-workflow
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To define and run workflows, you can create tasks by inheriting from the Task class and implementing the _execute method. Here's an example of how to define a simple addition task:
```python
from at_common_workflow.core.task import Task
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
```

To run a workflow:
```python
from at_common_workflow.core.workflow import Workflow

workflow = Workflow()
task = AddTask("add_numbers")
workflow.add_task(task, arg_mappings={"a": 5, "b": 3}, result_mapping="result")
await workflow.execute()
print(workflow.context.get("result").result)  # Output: 8
```

## Testing
To run the tests, use the following command:
```bash
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.

## License
This project is licensed under the [MIT License](LICENSE).