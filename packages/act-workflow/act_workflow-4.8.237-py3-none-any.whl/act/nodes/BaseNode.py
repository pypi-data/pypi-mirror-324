import os
import json
import logging
from typing import Dict, Any, Optional
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BaseNode:
    def __init__(self, sandbox_timeout: Optional[int] = None):
        """
        Initialize the base node.
        :param sandbox_timeout: Optional timeout for sandboxed execution.
        """
        logger.info("Initializing BaseNode")
        self.sandbox_timeout = sandbox_timeout

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the node's main functionality. This should be overridden by subclasses.
        :param node_data: The input data for the node.
        :return: The result of the node execution.
        """
        raise NotImplementedError("The execute method must be implemented by subclasses.")

    def validate_params(self, required_params: list, node_data: Dict[str, Any]) -> bool:
        """
        Validate that required parameters are present in node_data.
        :param required_params: List of required parameter names.
        :param node_data: The node's data.
        :return: True if all required parameters are present, otherwise raises an exception.
        """
        missing_params = [param for param in required_params if param not in node_data.get("params", {})]
        if missing_params:
            error_message = f"Missing required parameters: {', '.join(missing_params)}"
            logger.error(error_message)
            raise ValueError(error_message)
        return True

    def resolve_placeholders(self, text: str, node_data: Dict[str, Any]) -> str:
        """
        Resolve placeholders in a string using the node_data context.
        :param text: The text with placeholders.
        :param node_data: The context data to resolve placeholders.
        :return: The text with placeholders replaced by actual values.
        """
        pattern = re.compile(r"\{\{(.*?)\}\}")
        matches = pattern.findall(text)

        for match in matches:
            parts = match.split('.')
            value = self.fetch_value(parts, node_data)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))

        return text

    def fetch_value(self, path_parts: list, node_data: Dict[str, Any]) -> Any:
        """
        Fetch a value from the node_data using a list of keys.
        :param path_parts: List of keys representing the path to the value.
        :param node_data: The data to fetch the value from.
        :return: The value if found, otherwise None.
        """
        value = node_data
        try:
            for part in path_parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return None
            return value
        except Exception as e:
            logger.error(f"Error fetching value for path {'.'.join(path_parts)}: {e}")
            return None

    def extract_text(self, input_text: Any) -> str:
        """
        Extract actual text from input, handling JSON and other formats.
        :param input_text: The input text to process.
        :return: The extracted text.
        """
        try:
            if isinstance(input_text, str):
                parsed = json.loads(input_text)
                if isinstance(parsed, dict):
                    return parsed.get('value', input_text)
            elif isinstance(input_text, dict):
                return input_text.get('value', str(input_text))
        except (json.JSONDecodeError, ValueError):
            pass
        return str(input_text)

    def log_safe_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redact sensitive information (like API keys) from logs.
        :param data: The data to sanitize.
        :return: A sanitized version of the data.
        """
        if isinstance(data, dict):
            return {k: ('[REDACTED]' if 'key' in k.lower() else v) for k, v in data.items()}
        return data

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle an error and return a formatted error response.
        :param error: The exception to handle.
        :param context: Additional context about where the error occurred.
        :return: A dictionary containing the error details.
        """
        error_message = f"Error in {context}: {str(error)}"
        logger.error(error_message)
        return {"status": "error", "message": error_message}

if __name__ == "__main__":
    # Example usage of BaseNode for testing purposes
    class ExampleNode(BaseNode):
        def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
            try:
                # Validate required parameters
                self.validate_params(["example_param"], node_data)

                # Extract and process input text
                input_text = self.extract_text(node_data.get("params", {}).get("example_param"))
                logger.info(f"Processing input: {input_text}")

                # Resolve placeholders in text
                resolved_text = self.resolve_placeholders(input_text, node_data)
                logger.info(f"Resolved text: {resolved_text}")

                # Return success result
                return {"status": "success", "result": {"processed_text": resolved_text}}

            except Exception as e:
                return self.handle_error(e, context="ExampleNode execution")

    # Test example node
    example_node = ExampleNode()
    test_data = {
        "params": {
            "example_param": "Hello, {{user.name}}!"
        },
        "input": {
            "user": {
                "name": "Taj"
            }
        }
    }
    result = example_node.execute(test_data)
    print(json.dumps(result, indent=2))