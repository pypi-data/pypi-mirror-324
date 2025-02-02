import json
import logging
from typing import Dict, Any
from base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SwitchNode(BaseNode):
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the SwitchNode to determine the path based on a key-value mapping.
        :param node_data: The input data for the node.
        :return: A dictionary containing the selected path.
        """
        try:
            # Validate required parameters
            self.validate_params(["switch_key", "cases", "default_path"], node_data)

            # Extract parameters
            switch_key = node_data["params"].get("switch_key")
            resolved_key = self.resolve_placeholders(switch_key, node_data)
            logger.info(f"Resolved switch key: {resolved_key}")

            cases = node_data["params"].get("cases", {})
            default_path = node_data["params"].get("default_path")

            # Determine the path based on the resolved key
            next_path = cases.get(resolved_key, default_path)
            if not next_path:
                raise ValueError(f"No matching path found for key '{resolved_key}', and no default path specified.")

            logger.info(f"Next path selected: {next_path}")

            return {
                "status": "success",
                "result": {
                    "switch_key": resolved_key,
                    "next_path": next_path
                }
            }

        except Exception as e:
            return self.handle_error(e, context="SwitchNode execution")

if __name__ == "__main__":
    # Example usage of SwitchNode
    switch_node = SwitchNode()
    test_data = {
        "params": {
            "switch_key": "{{input.status}}",
            "cases": {
                "success": "path_success",
                "error": "path_error",
                "pending": "path_pending"
            },
            "default_path": "path_default"
        },
        "input": {
            "status": "success"
        }
    }
    result = switch_node.execute(test_data)
    print(json.dumps(result, indent=2))
