import json
import logging
from .base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class StartNode(BaseNode):
    def execute(self, node_data):
        """
        Executes the StartNode logic.
        """
        logger.info("Executing StartNode...")

        # Validate required parameters
        start_params = node_data.get("params", {})
        output_field = node_data.get("output_field", "start_data")

        try:
            # Optionally, generate initial data or return predefined data
            start_data = self._generate_initial_data(start_params)
            return {
                "status": "success",
                "message": "StartNode executed successfully",
                "result": {output_field: start_data}
            }
        except Exception as e:
            logger.error(f"Error during StartNode execution: {e}")
            return {"status": "error", "message": str(e)}

    def _generate_initial_data(self, params):
        """
        Generates initial data for the workflow. Can be static or dynamic based on `params`.
        """
        initial_value = params.get("initial_value", "default_value")
        additional_data = params.get("additional_data", {})
        return {
            "initial_value": initial_value,
            "additional_data": additional_data
        }

if __name__ == "__main__":
    # Example usage
    start_node = StartNode()
    test_data = {
        "params": {
            "initial_value": "Hello, Workflow!",
            "additional_data": {"key1": "value1", "key2": "value2"}
        },
        "output_field": "start_output"
    }
    result = start_node.execute(test_data)
    print(json.dumps(result, indent=2))
