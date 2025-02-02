import json
import logging
from typing import Dict, Any
from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class IfNode(BaseNode):
    """
    A simple node that checks a condition (true/false) 
    and returns different outputs accordingly.
    """

    def get_schema(self) -> NodeSchema:
        """
        Returns the schema describing this node's parameters and outputs.
        """
        return NodeSchema(
            node_type="if",
            version="1.0.0",
            description="Node for conditional logic based on a 'condition' parameter",
            parameters=[
                NodeParameter(
                    name="condition",
                    type=NodeParameterType.STRING,
                    description="Condition to evaluate (e.g. 'true'/'false')",
                    required=True
                ),
                NodeParameter(
                    name="data_if_true",
                    type=NodeParameterType.OBJECT,
                    description="Data returned if condition is true",
                    required=False,
                ),
                NodeParameter(
                    name="data_if_false",
                    type=NodeParameterType.OBJECT,
                    description="Data returned if condition is false",
                    required=False,
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
        Evaluate 'condition'. If it's in ('true', '1', 'yes') [case-insensitive], return the 'true' branch.
        Otherwise, return the 'false' branch.
        """
        try:
            logger.info("Executing IfNode...")

            # 1. Validate required fields
            if "condition" not in node_data:
                raise ValueError("Missing required field: condition")

            # 2. Extract parameters
            raw_condition = node_data["condition"]
            data_if_true = node_data.get("data_if_true", {})
            data_if_false = node_data.get("data_if_false", {})

            # 3. Evaluate condition (case-insensitive)
            condition_str = str(raw_condition).strip().lower()
            is_true = condition_str in ["true", "1", "yes"]

            # 4. Return different outputs depending on truth
            if is_true:
                return {
                    "status": "success",
                    "message": "Condition evaluated: True",
                    "result": {
                        "branch": "true",
                        "data": data_if_true
                    }
                }
            else:
                return {
                    "status": "success",
                    "message": "Condition evaluated: False",
                    "result": {
                        "branch": "false",
                        "data": data_if_false
                    }
                }

        except Exception as e:
            logger.error(f"Error in IfNode execution: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

if __name__ == "__main__":
    # Example usage
    node = IfNode()

    # If condition is 'true' => branch is 'true'
    test_data_true = {
        "condition": "TrUe",  # case-insensitive
        "data_if_true": {"example": "This is the true branch data"}
    }
    result_true = node.execute(test_data_true)
    print("=== TRUE CONDITION ===")
    print(json.dumps(result_true, indent=2))

    # If condition is 'false' => branch is 'false'
    test_data_false = {
        "condition": "no",  # not in ["true", "1", "yes"]
        "data_if_false": {"example": "This is the false branch data"}
    }
    result_false = node.execute(test_data_false)
    print("\n=== FALSE CONDITION ===")
    print(json.dumps(result_false, indent=2))
