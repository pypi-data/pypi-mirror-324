import json
import logging
import os
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import openai
from .base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAINode(BaseNode):
    """OpenAI Node with flat parameter structure."""

    def get_schema(self) -> NodeSchema:
        """Define the schema for OpenAI node."""
        return NodeSchema(
            node_type="openai",
            version="1.0.0",
            description="Node for processing requests to OpenAI's API",
            parameters=[
                NodeParameter(
                    name="api_key",
                    type=NodeParameterType.SECRET,
                    description="OpenAI API key (from environment)",
                    required=True,
                    pattern=r"^\${[A-Z_]+}$"  # Pattern for environment variable syntax
                ),
                NodeParameter(
                    name="input_text",
                    type=NodeParameterType.STRING,
                    description="Input text for the model",
                    required=True
                ),
                NodeParameter(
                    name="model",
                    type=NodeParameterType.STRING,
                    description="OpenAI model to use",
                    required=False,
                    default="gpt-4",
                    enum=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo-preview"]
                ),
                NodeParameter(
                    name="output_field",
                    type=NodeParameterType.STRING,
                    description="Field name for the output",
                    required=False,
                    default="response"
                ),
                NodeParameter(
                    name="temperature",
                    type=NodeParameterType.NUMBER,
                    description="Temperature for response generation",
                    required=False,
                    default=0.7,
                    min_value=0.0,
                    max_value=2.0
                ),
                NodeParameter(
                    name="max_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum tokens in response",
                    required=False,
                    min_value=1,
                    max_value=32000
                ),
                NodeParameter(
                    name="system_prompt",
                    type=NodeParameterType.STRING,
                    description="System prompt for the conversation",
                    required=False,
                    default="You are a helpful assistant."
                )
            ],
            outputs={
                "response": NodeParameterType.STRING,
                "model_used": NodeParameterType.STRING,
                "input_tokens": NodeParameterType.NUMBER
            }
        )

    def _resolve_env_vars(self, value: str) -> str:
        """Resolve environment variables in string values."""
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]  # Remove ${ and }
            resolved_value = os.getenv(env_var)
            if resolved_value is None:
                raise ValueError(f"Environment variable {env_var} not found")
            return resolved_value
        return value

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OpenAI request with flat parameter structure."""
        try:
            logger.info("Initializing OpenAINode execution...")

            # Resolve environment variables in parameters
            resolved_data = {}
            for key, value in node_data.items():
                resolved_data[key] = self._resolve_env_vars(value)

            # Validate API key format
            api_key = resolved_data.get("api_key")
            if not api_key or not api_key.startswith("sk-"):
                raise ValueError("Invalid OpenAI API key format")

            # Set OpenAI API key
            openai.api_key = api_key

            # Build request configuration
            config = {
                "input_text": resolved_data["input_text"],
                "model": resolved_data.get("model", "gpt-4"),
                "temperature": resolved_data.get("temperature", 0.7),
                "max_tokens": resolved_data.get("max_tokens"),
                "system_prompt": resolved_data.get("system_prompt", "You are a helpful assistant.")
            }

            # Send request to OpenAI
            response = self._send_request(config)

            # Build result with specified output field
            output_field = resolved_data.get("output_field", "response")
            result = {
                "status": "success",
                "message": "OpenAI API call succeeded",
                "result": {
                    output_field: response,
                    "model_used": config["model"],
                    "input_tokens": self._estimate_tokens(config["input_text"])
                }
            }

            logger.info("Execution completed successfully")
            return result

        except Exception as e:
            error_context = "OpenAINode execution"
            logger.error(f"Error in {error_context}: {str(e)}", exc_info=True)
            return self.handle_error(e, error_context)

    def _send_request(self, config: Dict[str, Any]) -> str:
        """Send request to OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": config["system_prompt"]},
                {"role": "user", "content": config["input_text"]}
            ]

            response = openai.ChatCompletion.create(
                model=config["model"],
                messages=messages,
                temperature=config["temperature"],
                max_tokens=config.get("max_tokens"),
                n=1,
                stream=False
            )

            return response.choices[0].message["content"]

        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens in text."""
        return len(text) // 4

# Example usage
if __name__ == "__main__":
    test_data = {
        "api_key": "${OPENAI_API_KEY}",
        "input_text": "give me a joke",
        "model": "gpt-4",
        "output_field": "openai_generated_data"
    }

    node = OpenAINode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))