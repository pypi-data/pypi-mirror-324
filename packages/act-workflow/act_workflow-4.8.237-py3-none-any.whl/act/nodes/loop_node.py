import json
import logging
from typing import Dict, Any, List
from base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LoopNode(BaseNode):
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the LoopNode to process each item in a list iteratively.
        :param node_data: The input data for the node.
        :return: A dictionary containing the results of the loop execution.
        """
        try:
            # Validate required parameters
            self.validate_params(["list", "operation"], node_data)

            # Get the list to iterate over
            input_list = node_data["params"].get("list")
            if not isinstance(input_list, list):
                raise ValueError("The 'list' parameter must be a list.")

            # Get the operation template
            operation_template = node_data["params"].get("operation")

            # Process each item in the list
            results = []
            for idx, item in enumerate(input_list):
                logger.info(f"Processing item {idx + 1}/{len(input_list)}: {item}")

                # Create a dynamic context for placeholder resolution
                context = {"item": item, "index": idx}
                resolved_operation = self.resolve_placeholders(operation_template, {"context": context})

                # Execute the resolved operation (e.g., eval, API call, etc.)
                # In a real scenario, this could involve dynamic node execution or external API calls
                logger.info(f"Resolved operation: {resolved_operation}")
                results.append({"item": item, "result": resolved_operation})

            return {
                "status": "success",
                "result": {
                    "processed_items": results
                }
            }

        except Exception as e:
            return self.handle_error(e, context="LoopNode execution")

if __name__ == "__main__":
    # Example usage of LoopNode
    loop_node = LoopNode()
    test_data = {
        "params": {
            "list": ["apple", "banana", "cherry"],
            "operation": "Processed {{context.item}} at index {{context.index}}"
        }
    }
    result = loop_node.execute(test_data)
    print(json.dumps(result, indent=2))