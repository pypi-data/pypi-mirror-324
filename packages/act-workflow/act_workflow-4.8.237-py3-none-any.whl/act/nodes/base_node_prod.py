import os
import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# -------------------------
# Custom Exceptions
# -------------------------
class NodeError(Exception):
    """Base exception for node errors."""
    pass

class NodeValidationError(NodeError):
    """Raised when node validation fails."""
    pass

class NodeExecutionError(NodeError):
    """Raised when node execution fails."""
    pass

# -------------------------
# Enum & Models for Schema
# -------------------------
class NodeParameterType(str, Enum):
    """Enum defining possible parameter types for node inputs."""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    SECRET = "secret"

class NodeParameter(BaseModel):
    """Defines a single parameter for a node."""
    name: str
    type: NodeParameterType
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None

    @validator('default')
    def validate_default_value(cls, v, values):
        if v is not None:
            param_type = values.get('type')
            if param_type == NodeParameterType.STRING and not isinstance(v, str):
                raise ValueError("Default value must be a string")
            elif param_type == NodeParameterType.NUMBER and not isinstance(v, (int, float)):
                raise ValueError("Default value must be a number")
            elif param_type == NodeParameterType.BOOLEAN and not isinstance(v, bool):
                raise ValueError("Default value must be a boolean")
        return v

class NodeSchema(BaseModel):
    """Base schema definition for a node."""
    node_type: str
    version: str
    description: str
    parameters: List[NodeParameter]
    outputs: Dict[str, NodeParameterType]
    children: Optional[List["NodeSchema"]] = None  # For nested/composite nodes

    class Config:
        extra = "allow"  # Allow extra fields for future extension

# Update forward references for nested schema
NodeSchema.update_forward_refs()

# -------------------------
# Base Node Definition
# -------------------------
class BaseNode(ABC):
    """Enhanced base node with schema support and extensibility."""
    
    def __init__(self, sandbox_timeout: Optional[int] = None, dependencies: Optional[Dict[str, Any]] = None):
        logger.info("Initializing BaseNode")
        self.sandbox_timeout = sandbox_timeout
        self.dependencies = dependencies or {}
        self._schema = self.get_schema()
        self.children: List[BaseNode] = []  # For composite nodes

    @abstractmethod
    def get_schema(self) -> NodeSchema:
        """Return the schema definition for this node."""
        pass

    def validate_schema(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data against the node's schema.
        :param node_data: The input data to validate.
        :return: Validated and processed data.
        """
        validated_data = {}
        params = node_data.get("params", {})

        try:
            for param in self._schema.parameters:
                value = params.get(param.name)

                # Handle required parameters
                if param.required and value is None:
                    raise NodeValidationError(f"Missing required parameter: {param.name}")

                # Apply default value if needed
                if value is None and param.default is not None:
                    value = param.default

                # Skip if no value and not required
                if value is None and not param.required:
                    continue

                # Type validation
                self._validate_type(param, value)

                # Range validation for numbers
                if param.type == NodeParameterType.NUMBER:
                    self._validate_range(param, value)

                # Enum validation
                if param.enum is not None and value not in param.enum:
                    raise NodeValidationError(f"Parameter {param.name} must be one of: {param.enum}")

                # Pattern validation for strings
                if param.pattern is not None and param.type == NodeParameterType.STRING:
                    if not re.match(param.pattern, value):
                        raise NodeValidationError(f"Parameter {param.name} does not match required pattern")

                validated_data[param.name] = value

            # Allow node-specific custom validation
            custom_data = self.validate_custom(node_data)
            validated_data.update(custom_data)
            return validated_data

        except Exception as e:
            raise NodeValidationError(f"Schema validation error: {str(e)}")

    def validate_custom(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Node-specific custom validation. Override this in subclasses if needed.
        """
        return {}

    def _validate_type(self, param: NodeParameter, value: Any):
        """Validate parameter type."""
        if param.type == NodeParameterType.STRING and not isinstance(value, str):
            raise NodeValidationError(f"Parameter {param.name} must be a string")
        elif param.type == NodeParameterType.NUMBER and not isinstance(value, (int, float)):
            raise NodeValidationError(f"Parameter {param.name} must be a number")
        elif param.type == NodeParameterType.BOOLEAN and not isinstance(value, bool):
            raise NodeValidationError(f"Parameter {param.name} must be a boolean")
        elif param.type == NodeParameterType.ARRAY and not isinstance(value, list):
            raise NodeValidationError(f"Parameter {param.name} must be an array")
        elif param.type == NodeParameterType.OBJECT and not isinstance(value, dict):
            raise NodeValidationError(f"Parameter {param.name} must be an object")

    def _validate_range(self, param: NodeParameter, value: Any):
        """Validate numeric range."""
        if param.min_value is not None and value < param.min_value:
            raise NodeValidationError(f"Parameter {param.name} must be >= {param.min_value}")
        if param.max_value is not None and value > param.max_value:
            raise NodeValidationError(f"Parameter {param.name} must be <= {param.max_value}")

    def validate_params(self, required_params: list, node_data: Dict[str, Any]) -> bool:
        """
        Legacy parameter validation method for backward compatibility.
        """
        missing_params = [param for param in required_params if param not in node_data.get("params", {})]
        if missing_params:
            error_message = f"Missing required parameters: {', '.join(missing_params)}"
            logger.error(error_message)
            raise NodeValidationError(error_message)
        return True

    def resolve_placeholders(self, text: str, node_data: Dict[str, Any]) -> str:
        """Resolve placeholders in a string using the node_data context."""
        pattern = re.compile(r"\{\{(.*?)\}\}")
        matches = pattern.findall(text)

        for match in matches:
            parts = match.split('.')
            value = self.fetch_value(parts, node_data)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))
        return text

    def fetch_value(self, path_parts: list, node_data: Dict[str, Any]) -> Any:
        """Fetch a value from the node_data using a list of keys."""
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
        """Extract actual text from input, handling JSON and other formats."""
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
        """Redact sensitive information from logs."""
        if isinstance(data, dict):
            return {k: ('[REDACTED]' if 'key' in k.lower() else v) for k, v in data.items()}
        return data

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle an error and return a formatted error response."""
        error_message = f"Error in {context}: {str(error)}"
        logger.error(error_message)
        return {"status": "error", "message": error_message}

    def add_child(self, child: "BaseNode"):
        """Add a child node for composite execution."""
        self.children.append(child)

    async def execute_children(self, node_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute all child nodes asynchronously and return their results."""
        results = []
        for child in self.children:
            result = await child.execute(node_data)
            results.append(result)
        return results

    @abstractmethod
    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the node's main functionality asynchronously."""
        pass

# -------------------------
# Node Registry (Plugin Factory)
# -------------------------
class NodeRegistry:
    _registry = {}

    @classmethod
    def register(cls, node_type: str, node_cls):
        cls._registry[node_type] = node_cls
        logger.info(f"Registered node type: {node_type}")

    @classmethod
    def create_node(cls, node_type: str, **kwargs) -> BaseNode:
        node_cls = cls._registry.get(node_type)
        if not node_cls:
            raise NodeError(f"Node type {node_type} is not registered.")
        return node_cls(**kwargs)

# -------------------------
# Example Node Implementation
# -------------------------
class ExampleNode(BaseNode):
    def get_schema(self) -> NodeSchema:
        return NodeSchema(
            node_type="example",
            version="1.0.0",
            description="Example node that processes text with placeholders",
            parameters=[
                NodeParameter(
                    name="example_param",
                    type=NodeParameterType.STRING,
                    description="Input text with optional placeholders",
                    required=True
                )
            ],
            outputs={
                "processed_text": NodeParameterType.STRING
            }
        )

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate schema and parameters
            validated_data = self.validate_schema(node_data)
            # Extract and process input text
            input_text = self.extract_text(validated_data["example_param"])
            logger.info(f"Processing input: {input_text}")

            # Resolve placeholders using the full node_data context
            resolved_text = self.resolve_placeholders(input_text, node_data)
            logger.info(f"Resolved text: {resolved_text}")

            # If there are child nodes, execute them asynchronously
            children_results = await self.execute_children(node_data) if self.children else []

            # Return success result along with any children outputs
            return {
                "status": "success",
                "result": {
                    "processed_text": resolved_text,
                    "children_results": children_results
                }
            }
        except Exception as e:
            return self.handle_error(e, context="ExampleNode execution")

# Register ExampleNode in the registry
NodeRegistry.register("example", ExampleNode)

# -------------------------
# Main Block for Testing
# -------------------------
if __name__ == "__main__":
    async def main():
        # Create an example node via the registry
        example_node = NodeRegistry.create_node("example")
        
        # Print the node schema (formatted as JSON)
        print("Node Schema:")
        print(example_node.get_schema().json(indent=2))
        
        # Test execution with sample data
        test_data = {
            "params": {
                "example_param": "Hello, {{input.user.name}}!"
            },
            "input": {
                "user": {
                    "name": "Taj"
                }
            }
        }
        
        print("\nExecution Result:")
        result = await example_node.execute(test_data)
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
