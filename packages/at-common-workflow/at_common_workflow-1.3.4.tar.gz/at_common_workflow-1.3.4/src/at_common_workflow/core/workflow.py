from typing import List, Dict, Union, Any, Set, Optional, Callable
from at_common_workflow.core.context import Context
from at_common_workflow.core.task import Task
from at_common_workflow.utils import ArgumentMapping, ResultMapping
import asyncio
from at_common_workflow.types.constants import TaskStatus
from at_common_workflow.core.task_node import TaskNode
from at_common_workflow.core.workflow_progress import WorkflowProgress

class Workflow:
    """Orchestrates the execution of tasks in a directed acyclic graph with parallel execution support."""
    
    def __init__(self):
        self.tasks: List[TaskNode] = []
        self.context = Context()
        self.progress = WorkflowProgress()
        self.on_task_start: Optional[Callable[[str], None]] = None
        self.on_task_complete: Optional[Callable[[str], None]] = None
        self.on_task_error: Optional[Callable[[str, Exception], None]] = None
        self._task_dependencies: Dict[str, Set[str]] = {}
        self._reverse_dependencies: Dict[str, Set[str]] = {}
    
    def add_task(
        self,
        task: Task,
        argument_mappings: Dict[str, ArgumentMapping],
        result_mapping: ResultMapping
    ) -> None:
        """
        Add a task to the workflow with its argument mappings and result mapping.
        
        Args:
            task: The task to add
            argument_mappings: Dictionary mapping argument names to either:
                         - Context references (strings starting with $)
                         - Constant values
            result_mapping: Either:
                          - A string for the context key to store the entire result
                          - A tuple of (context_key, result_path) to store a specific field
        """           
        task_node = TaskNode(task, argument_mappings, result_mapping)
        self.tasks.append(task_node)
        self._task_dependencies[task.name] = set()
        self._reverse_dependencies[task.name] = set()
    
    def _build_dependency_graph(self) -> None:
        """Build the dependency graph based on context references."""
        context_providers = {}
        referenced_keys = set()

        # First pass: collect all context providers and referenced keys
        for task_node in self.tasks:
            # Track providers
            context_key = task_node.result_mapping.context_key
            if context_key in context_providers:
                raise ValueError(
                    f"Multiple tasks trying to write to context key '{context_key}'"
                )
            context_providers[context_key] = task_node.task.name

            # Track references
            for arg_mapping in task_node.argument_mappings.values():
                if arg_mapping.is_context_ref:
                    referenced_keys.add(arg_mapping.value[1:])  # Remove $ prefix

        # Check for references to future task results
        for key in referenced_keys:
            if key in context_providers:
                continue
            # If the key is in the format "resultX" where X is a number, it's likely a reference to a future task
            if key.startswith("result"):
                raise ValueError(f"References undefined context key '{key}'")

        # Initialize dependency dictionaries for all tasks
        self._task_dependencies.clear()
        self._reverse_dependencies.clear()
        for task_node in self.tasks:
            task_name = task_node.task.name
            self._task_dependencies[task_name] = set()
            self._reverse_dependencies[task_name] = set()

        # Second pass: build dependencies based on context references
        for task_node in self.tasks:
            task_name = task_node.task.name

            # Check context references in arguments
            for arg_name, arg_mapping in task_node.argument_mappings.items():
                if arg_mapping.is_context_ref:
                    context_key = arg_mapping.value[1:]  # Remove $ prefix
                    if context_key in context_providers:
                        provider_task = context_providers[context_key]
                        self._task_dependencies[task_name].add(provider_task)
                        self._reverse_dependencies[provider_task].add(task_name)
                    # Missing context keys that aren't future task results will be caught during execution

        # Check for cycles in the dependency graph
        visited = set()
        temp_visited = set()
        
        def has_cycle(task_name: str) -> bool:
            if task_name in temp_visited:
                return True
            if task_name in visited:
                return False
            
            temp_visited.add(task_name)
            
            for dep in self._task_dependencies[task_name]:
                if has_cycle(dep):
                    return True
                    
            temp_visited.remove(task_name)
            visited.add(task_name)
            return False
        
        for task_name in self._task_dependencies:
            if has_cycle(task_name):
                raise ValueError(f"Cyclic dependencies detected in workflow: task '{task_name}' is part of a cycle")

    def _get_ready_tasks(self, completed_tasks: Set[str]) -> Set[str]:
        """Get tasks whose dependencies are all satisfied and required context keys are available."""
        ready_tasks = set()
        for task_node in self.tasks:
            task_name = task_node.task.name
            if (task_name in completed_tasks or 
                self.progress.task_statuses.get(task_name, TaskStatus.PENDING) != TaskStatus.PENDING):
                continue

            dependencies = self._task_dependencies[task_name]
            if all(dep in completed_tasks for dep in dependencies):
                # Check context availability
                all_context_available = True
                for arg_mapping in task_node.argument_mappings.values():
                    if arg_mapping.is_context_ref:
                        context_key = arg_mapping.value[1:]  # Remove $ prefix
                        if context_key not in self.context:
                            all_context_available = False
                            break
                if all_context_available:
                    ready_tasks.add(task_name)
        return ready_tasks

    async def _execute_task(self, task_name: str) -> None:
        """Execute a single task and update its status."""
        task_node = next(t for t in self.tasks if t.task.name == task_name)
        
        self.progress.update_task_status(task_name, TaskStatus.RUNNING)
        if self.on_task_start:
            self.on_task_start(task_name)
            
        try:
            # Resolve arguments
            args = {
                name: mapping.resolve(self.context)
                for name, mapping in task_node.argument_mappings.items()
            }
            
            # Execute task
            result = await task_node.task(**args)
            task_node.result_mapping.store(self.context, result)
            self.progress.update_task_status(task_name, TaskStatus.COMPLETED)
            if self.on_task_complete:
                self.on_task_complete(task_name)
        except Exception as e:
            self.progress.update_task_status(task_name, TaskStatus.FAILED)
            if self.on_task_error:
                self.on_task_error(task_name, e)
            raise

    async def execute(self) -> Context:
        """
        Execute tasks in parallel when possible based on their dependencies.
        Returns the final context.
        """
        self._build_dependency_graph()
        
        completed_tasks: Set[str] = set()
        running_tasks = set()
        tasks_in_progress = set()
        
        while len(completed_tasks) < len(self.tasks):
            # Get tasks that are ready to run
            ready_tasks = self._get_ready_tasks(completed_tasks) - tasks_in_progress
            
            if not ready_tasks and not tasks_in_progress:
                remaining_tasks = {t.task.name for t in self.tasks} - completed_tasks
                raise RuntimeError(f"Unable to make progress. Tasks stuck: {remaining_tasks}")
            
            # Start new tasks
            running_tasks = set()
            for task_name in ready_tasks:
                running_tasks.add(asyncio.create_task(self._execute_task(task_name)))
                tasks_in_progress.add(task_name)
            
            if running_tasks:
                # Wait for at least one task to complete
                done, _ = await asyncio.wait(running_tasks, return_when=asyncio.FIRST_COMPLETED)
                
                # Process completed tasks
                for task in done:
                    try:
                        await task
                        # Find which task completed
                        completed_task_name = next(
                            name for name in tasks_in_progress 
                            if self.progress.task_statuses[name] == TaskStatus.COMPLETED
                        )
                        completed_tasks.add(completed_task_name)
                        tasks_in_progress.remove(completed_task_name)
                    except Exception as e:
                        # If any task fails, propagate the error
                        raise RuntimeError("Workflow execution failed") from e
            
        return self.context

    def get_initial_context_schema(self) -> Dict[str, Any]:
        """
        Analyze tasks to determine required initial context values.
        Returns a dictionary describing the required context structure.
        """
        # Build dependency graph to ensure proper analysis order
        self._build_dependency_graph()
        
        # Track what each task provides to context
        provided_keys = {}  # context_key -> task_name
        required_keys = set()
        
        # First pass: collect all context providers
        for task_node in self.tasks:
            context_key = task_node.result_mapping.context_key
            provided_keys[context_key] = task_node.task.name
        
        # Second pass: analyze required context keys
        for task_node in self.tasks:
            for arg_mapping in task_node.argument_mappings.values():
                if arg_mapping.is_context_ref:
                    context_key = arg_mapping.value[1:]  # Remove $ prefix
                    # If this key isn't provided by any task, it must be initial input
                    if context_key not in provided_keys:
                        required_keys.add(context_key)
        
        # Build schema structure
        schema = {}
        for key in required_keys:
            current = schema
            parts = key.split('.')
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = "required"  # Could be enhanced with type info
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        
        return schema