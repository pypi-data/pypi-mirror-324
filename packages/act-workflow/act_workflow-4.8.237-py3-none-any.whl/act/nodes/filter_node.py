import os
import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional, List

# Import the base node definitions from your existing module.
from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FilterNode(BaseNode):
    def get_schema(self) -> NodeSchema:
        """
        Returns the schema for the FilterNode.
        This node expects:
          - input_data: an array of items to filter.
          - filter_condition: a string containing a Python expression that will be evaluated
                              in a context where each item is accessible via 'item'.
        """
        return NodeSchema(
            node_type="filter",
            version="1.0.0",
            description="Filters input data based on a provided condition",
            parameters=[
                NodeParameter(
                    name="input_data",
                    type=NodeParameterType.ARRAY,
                    description="Data to be filtered (list of dicts or similar)",
                    required=True
                ),
                NodeParameter(
                    name="filter_condition",
                    type=NodeParameterType.STRING,
                    description="A Python expression (using placeholders) to filter data. "
                                "Example: '{{item.value}} > 100'",
                    required=True
                )
            ],
            outputs={
                "filtered_data": NodeParameterType.ARRAY
            }
        )

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the FilterNode.
        Validates the input data against the schema, then iterates over each item in input_data.
        It resolves the filter condition for each item and uses eval() (with restricted __builtins__)
        to determine if the item passes the filter.
        Returns a success response with the filtered_data list.
        """
        try:
            # Validate the input against the node's schema.
            validated_data = self.validate_schema(node_data)
            input_data = validated_data["input_data"]
            condition_template = validated_data["filter_condition"]

            if not isinstance(input_data, list):
                raise Exception("input_data must be a list")

            filtered_data = []
            # Iterate over each item and evaluate the filter condition.
            for item in input_data:
                # Create an evaluation context. The context is minimal for security.
                eval_context = {
                    'item': item,
                    'True': True,
                    'False': False,
                    'None': None
                }
                # Resolve placeholders (e.g., "{{item.value}}") using the current item.
                condition = self.resolve_placeholders(condition_template, {"item": item})
                # Evaluate the condition; if true, include the item in the results.
                if eval(condition, {"__builtins__": {}}, eval_context):
                    filtered_data.append(item)

            return {
                "status": "success",
                "result": {
                    "filtered_data": filtered_data
                }
            }
        except Exception as e:
            return self.handle_error(e, context="FilterNode execution")

# -------------------------
# Main Block for Testing
# -------------------------
if __name__ == "__main__":
    async def main():
        filter_node = FilterNode()  # Instantiating the FilterNode (now fully implemented)
        test_data = {
            "params": {
                "input_data": [{"value": 150}, {"value": 50}, {"value": 200}],
                "filter_condition": "{{item.value}} > 100"
            }
        }
        result = await filter_node.execute(test_data)
        print(json.dumps(result, indent=2))
    asyncio.run(main())
