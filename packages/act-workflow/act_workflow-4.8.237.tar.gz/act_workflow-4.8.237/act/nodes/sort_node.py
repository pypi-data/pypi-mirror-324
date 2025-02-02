import os
import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional, List

# Import base node definitions from your module.
from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SortNode(BaseNode):
    def get_schema(self) -> NodeSchema:
        """
        Returns the schema for the SortNode.
        This node expects:
          - data: an array of numbers to sort.
          - order: a string indicating the sort order ('asc' or 'desc').
        """
        return NodeSchema(
            node_type="sort",
            version="1.0.0",
            description="Sorts an array of numbers based on specified order",
            parameters=[
                NodeParameter(
                    name="data",
                    type=NodeParameterType.ARRAY,
                    description="Array of numbers to sort",
                    required=True
                ),
                NodeParameter(
                    name="order",
                    type=NodeParameterType.STRING,
                    description="Sorting order: 'asc' for ascending, 'desc' for descending",
                    required=False,
                    default="asc",
                    enum=["asc", "desc"]
                )
            ],
            outputs={
                "sorted_data": NodeParameterType.ARRAY
            }
        )

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the SortNode.
        Validates the input data and sorts the provided array based on the specified order.
        Returns the sorted array in the 'sorted_data' output.
        """
        try:
            # Validate input against the schema
            validated_data = self.validate_schema(node_data)
            data = validated_data["data"]
            order = validated_data.get("order", "asc")
            
            # Ensure data is a list
            if not isinstance(data, list):
                raise Exception("The 'data' parameter must be a list.")
            
            # Sort the list; reverse sort if order is 'desc'
            sorted_data = sorted(data, reverse=(order == "desc"))
            
            return {
                "status": "success",
                "result": {
                    "sorted_data": sorted_data
                }
            }
        except Exception as e:
            return self.handle_error(e, context="SortNode execution")

# -------------------------
# Main Block for Testing
# -------------------------
if __name__ == "__main__":
    async def main():
        sort_node = SortNode()  # Instantiate the SortNode
        test_data = {
            "params": {
                "data": [5, 3, 8, 1, 9],
                "order": "asc"  # Change to "desc" for descending order
            }
        }
        result = await sort_node.execute(test_data)
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
