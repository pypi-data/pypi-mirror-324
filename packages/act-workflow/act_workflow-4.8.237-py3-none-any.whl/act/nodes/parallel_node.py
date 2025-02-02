import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from .base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ParallelNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.execution_manager = None

    def set_execution_manager(self, execution_manager):
        """Set the execution manager for this node."""
        self.execution_manager = execution_manager

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes multiple target nodes in parallel.
        """
        try:
            logger.info("Executing ParallelNode...")
            logger.debug(f"Node data received: {node_data}")
            
            # Get and validate tasks list
            tasks = self._get_tasks(node_data)
            if not tasks:
                return {
                    "status": "error",
                    "message": "'tasks' must be a non-empty list of node names"
                }

            # Get configuration parameters with defaults
            max_concurrent = int(str(node_data.get("max_concurrent", 5)).strip('"\''))
            timeout = int(str(node_data.get("timeout", 300)).strip('"\''))

            # Get input context
            input_context = node_data.get("input", {})
            
            # Get original node configurations from workflow
            node_configs = {}
            if self.execution_manager and hasattr(self.execution_manager, 'workflow_data'):
                workflow_nodes = self.execution_manager.workflow_data.get('nodes', {})
                for task in tasks:
                    if task in workflow_nodes:
                        config = workflow_nodes[task]
                        # Clean string values in the configuration
                        node_configs[task] = self._clean_node_config(config)

            # Initialize results container
            results = {
                "parallel_execution": {},
                "completed_tasks": [],
                "failed_tasks": [],
                "skipped_tasks": []
            }

            # Execute tasks in parallel
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                task_results = loop.run_until_complete(
                    self._execute_parallel_tasks(
                        tasks=tasks,
                        node_configs=node_configs,
                        input_context=input_context,
                        max_concurrent=max_concurrent,
                        timeout=timeout
                    )
                )
                
                # Process results
                for task_name, task_result in task_results.items():
                    results["parallel_execution"][task_name] = task_result
                    if task_result.get("status") == "success":
                        results["completed_tasks"].append(task_name)
                    else:
                        results["failed_tasks"].append(task_name)

            finally:
                loop.close()

            # Determine overall status
            if results["failed_tasks"]:
                status = "error"
                message = f"Some tasks failed: {', '.join(results['failed_tasks'])}"
            else:
                status = "success"
                message = "All parallel tasks completed successfully"

            return {
                "status": status,
                "message": message,
                "result": results
            }

        except Exception as e:
            logger.error(f"Error in ParallelNode execution: {str(e)}")
            return {
                "status": "error",
                "message": f"Error during parallel execution: {str(e)}"
            }

    def _clean_node_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively clean string values in node configuration."""
        cleaned = {}
        for key, value in config.items():
            if isinstance(value, dict):
                cleaned[key] = self._clean_node_config(value)
            elif isinstance(value, list):
                cleaned[key] = [self._clean_value(item) for item in value]
            else:
                cleaned[key] = self._clean_value(value)
        return cleaned

    def _clean_value(self, value: Any) -> Any:
        """Clean a single value, removing quotes from strings."""
        if isinstance(value, str):
            return value.strip('"\'')
        return value

    def _get_tasks(self, node_data: Dict[str, Any]) -> List[str]:
        """Extract and validate tasks from node data."""
        tasks = node_data.get("tasks", [])
        
        # Handle different input formats
        if isinstance(tasks, str):
            try:
                tasks = json.loads(tasks.strip('"\''))
            except json.JSONDecodeError:
                tasks = [t.strip() for t in tasks.strip('[]"\'').split(',') if t.strip()]

        # Ensure we have a list
        if not isinstance(tasks, list):
            tasks = [tasks] if tasks else []

        return [str(task).strip('"\'') for task in tasks if task]

    async def _execute_parallel_tasks(
        self,
        tasks: List[str],
        node_configs: Dict[str, Any],
        input_context: Dict[str, Any],
        max_concurrent: int,
        timeout: int
    ) -> Dict[str, Any]:
        """Execute tasks in parallel with controlled concurrency."""
        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_task(task_name: str) -> Dict[str, Any]:
            try:
                async with semaphore:
                    logger.info(f"Starting execution of task: {task_name}")
                    
                    if task_name not in node_configs:
                        return {
                            "status": "error",
                            "message": f"Configuration for task {task_name} not found"
                        }

                    # Get the original node configuration
                    task_config = node_configs[task_name]
                    
                    # Merge input context with original configuration
                    execution_data = {
                        **task_config,
                        "input": input_context
                    }

                    # Execute the task
                    if self.execution_manager and hasattr(self.execution_manager, "execute_node"):
                        result = self.execution_manager.execute_node(task_name, execution_data)
                        logger.info(f"Task {task_name} completed with status: {result.get('status')}")
                        return result
                    else:
                        return {
                            "status": "error",
                            "message": f"Unable to execute task {task_name}: execution manager not available"
                        }

            except Exception as e:
                logger.error(f"Error executing task {task_name}: {str(e)}")
                return {
                    "status": "error",
                    "message": f"Task execution failed: {str(e)}"
                }

        # Create tasks
        tasks_to_execute = [execute_task(task) for task in tasks]
        
        try:
            # Execute all tasks with timeout
            completed_tasks = await asyncio.wait_for(
                asyncio.gather(*tasks_to_execute, return_exceptions=True),
                timeout=timeout
            )
            
            # Process results
            for task_name, result in zip(tasks, completed_tasks):
                if isinstance(result, Exception):
                    results[task_name] = {
                        "status": "error",
                        "message": f"Task failed with error: {str(result)}"
                    }
                else:
                    results[task_name] = result

        except asyncio.TimeoutError:
            for task_name in tasks:
                if task_name not in results:
                    results[task_name] = {
                        "status": "error",
                        "message": f"Task execution timed out after {timeout} seconds"
                    }

        return results

if __name__ == "__main__":
    # Example usage
    node = ParallelNode()
    test_data = {
        "tasks": ["request_node", "delay_node"],
        "max_concurrent": 3,
        "timeout": 300,
        "input": {
            "result": {
                "some_data": "test_value"
            }
        }
    }
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))