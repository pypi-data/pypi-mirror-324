import json
import logging
from .base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SplitNode(BaseNode):
    def execute(self, node_data):
        """
        Splits input data into multiple outputs based on a given strategy.
        """
        logger.info("Executing SplitNode...")

        # Validate required parameters
        input_data = node_data.get("input_data")
        split_strategy = node_data.get("split_strategy", "equal").lower()
        split_param = node_data.get("split_param", None)
        output_field = node_data.get("output_field", "split_results")

        if not input_data or not isinstance(input_data, list):
            return {"status": "error", "message": "'input_data' must be a list"}
        if split_strategy not in ["equal", "key", "chunk"]:
            return {"status": "error", "message": f"Unsupported split strategy: {split_strategy}"}

        try:
            split_results = self._split_data(input_data, split_strategy, split_param)
            return {
                "status": "success",
                "message": "Splitting completed successfully",
                "result": {output_field: split_results}
            }
        except Exception as e:
            logger.error(f"Error during splitting: {e}")
            return {"status": "error", "message": str(e)}

    def _split_data(self, data, strategy, param):
        """
        Splits the data based on the specified strategy and parameter.
        """
        if strategy == "equal":
            # Split into equal parts
            num_splits = param if isinstance(param, int) and param > 0 else 2
            chunk_size = len(data) // num_splits
            return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        elif strategy == "key":
            # Split based on a key's value
            if not isinstance(param, str):
                raise ValueError("'split_param' must be a string when using 'key' strategy")
            result = {}
            for item in data:
                key = item.get(param, "undefined")
                result.setdefault(key, []).append(item)
            return result

        elif strategy == "chunk":
            # Split into fixed-size chunks
            chunk_size = param if isinstance(param, int) and param > 0 else 1
            return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        raise ValueError(f"Unknown split strategy: {strategy}")

if __name__ == "__main__":
    # Example usage
    split_node = SplitNode()
    test_data = {
        "input_data": [
            {"id": 1, "type": "bug", "description": "Fix login bug"},
            {"id": 2, "type": "feature", "description": "Add dashboard"},
            {"id": 3, "type": "bug", "description": "Fix API timeout"},
            {"id": 4, "type": "task", "description": "Update dependencies"}
        ],
        "split_strategy": "key",
        "split_param": "type",
        "output_field": "split_by_type"
    }
    result = split_node.execute(test_data)
    print(json.dumps(result, indent=2))
