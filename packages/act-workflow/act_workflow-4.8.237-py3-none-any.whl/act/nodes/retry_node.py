import json
import time
import requests
import logging
from typing import Dict, Any
from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RetryNode(BaseNode):
    def get_schema(self) -> NodeSchema:
        """
        Provide the schema for RetryNode. Adjust parameters/outputs as needed.
        """
        return NodeSchema(
            node_type="retry",
            version="1.0.0",
            description="Node for retrying tasks a specified number of times with a delay",
            parameters=[
                NodeParameter(
                    name="max_retries",
                    type=NodeParameterType.STRING,
                    description="Maximum number of retry attempts",
                    required=False,
                    default="3"
                ),
                NodeParameter(
                    name="retry_delay",
                    type=NodeParameterType.STRING,
                    description="Delay (in seconds) between attempts",
                    required=False,
                    default="5"
                ),
                NodeParameter(
                    name="task",
                    type=NodeParameterType.OBJECT,
                    description="Task configuration to execute on each retry attempt",
                    required=False
                ),
                NodeParameter(
                    name="input",
                    type=NodeParameterType.OBJECT,
                    description="Additional input data",
                    required=False
                )
            ],
            outputs={
                "status": NodeParameterType.STRING,
                "message": NodeParameterType.STRING,
                "result": NodeParameterType.OBJECT
            }
        )

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the retry logic with proper attempt counting and error handling.
        """
        try:
            logger.info("Executing RetryNode...")
            logger.debug(f"Node data received: {node_data}")

            # Get and validate parameters
            max_retries = node_data.get("max_retries", "3").strip('"\'')
            retry_delay = node_data.get("retry_delay", "5").strip('"\'')
            task = node_data.get("task", {})

            # Convert parameters to integers
            try:
                max_retries = int(max_retries)
                retry_delay = int(retry_delay)
            except ValueError as e:
                return {
                    "status": "error",
                    "message": f"Invalid parameter values: {str(e)}"
                }

            # Parse task if it's a string
            if isinstance(task, str):
                task = task.strip('"\'')
                try:
                    # Try to parse as JSON
                    task = json.loads(task)
                except json.JSONDecodeError:
                    # Create a default task configuration
                    task = {
                        "type": "RequestNode",
                        "method": "GET",
                        "url": task if task else "https://httpbin.org/status/200",
                        "headers": {"Content-Type": "application/json"}
                    }

            # Get input from previous node
            input_data = node_data.get("input", {})
            
            # Initialize tracking variables
            attempts = 0
            execution_history = []

            # Execute retry loop
            while attempts < max_retries:
                try:
                    attempts += 1
                    logger.info(f"Retry attempt {attempts}/{max_retries}")
                    
                    # Execute the request
                    result = self._execute_request(task)
                    
                    # Record the attempt
                    execution_history.append({
                        "attempt": attempts,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "status": result.get("status", "error"),
                        "message": result.get("message", "Unknown error"),
                        "response": result.get("result", {})
                    })

                    # If we get a success response, return immediately
                    if result.get("status") == "success":
                        return {
                            "status": "success",
                            "message": f"Task completed successfully on attempt {attempts}",
                            "result": {
                                "attempts": attempts,
                                "execution_history": execution_history,
                                **result.get("result", {})
                            }
                        }

                    # If result.get("status") == "error", we might decide whether to retry or not
                    status_code = result.get("result", {}).get("status_code")
                    if status_code and 500 <= status_code < 600:
                        # Retry on server errors
                        logger.info(f"Server error {status_code} encountered, will retry")
                    else:
                        # For client errors or other issues, stop retrying
                        break

                    # If we're going to retry, wait first
                    if attempts < max_retries:
                        time.sleep(retry_delay)

                except Exception as e:
                    logger.error(f"Error on attempt {attempts}: {str(e)}")
                    execution_history.append({
                        "attempt": attempts,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "error",
                        "message": str(e)
                    })

                    if attempts < max_retries:
                        time.sleep(retry_delay)

            # If we get here, all retries failed
            return {
                "status": "error",
                "message": f"Task failed after {attempts} attempts",
                "result": {
                    "attempts": attempts,
                    "execution_history": execution_history
                }
            }

        except Exception as e:
            logger.error(f"Error in RetryNode execution: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def _execute_request(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an HTTP request with the given configuration."""
        try:
            method = task.get("method", "GET")
            url = task.get("url")
            headers = task.get("headers", {})
            data = task.get("body")

            if not url:
                raise ValueError("URL is required")

            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data
            )

            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers)
            }

            # Try to get JSON response, fall back to text if not JSON
            try:
                result["body"] = response.json()
            except Exception:
                result["body"] = response.text

            # Handle response based on status code
            if 200 <= response.status_code < 300:
                return {
                    "status": "success",
                    "message": f"Request completed with status code {response.status_code}",
                    "result": result
                }
            else:
                return {
                    "status": "error",
                    "message": f"{response.status_code} {response.reason} for url: {url}",
                    "result": result
                }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }

if __name__ == "__main__":
    # Example usage
    retry_node = RetryNode()
    test_data = {
        "max_retries": "3",
        "retry_delay": "2",
        "task": {
            "method": "GET",
            "url": "https://httpbin.org/status/500"
        }
    }
    result = retry_node.execute(test_data)
    print(json.dumps(result, indent=2))
