import json
import logging
from base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MergeNode(BaseNode):
    def execute(self, node_data):
        """
        Merges outputs from multiple nodes.
        """
        logger.info("Executing MergeNode...")

        # Validate required parameters
        source_nodes = node_data.get("source_nodes")
        merge_strategy = node_data.get("merge_strategy", "concatenate")
        context = node_data.get("input", {})

        if not source_nodes or not isinstance(source_nodes, list):
            return {"status": "error", "message": "'source_nodes' must be a list of node names"}

        if merge_strategy not in ["concatenate", "aggregate", "key_based"]:
            return {"status": "error", "message": f"Unsupported merge strategy: {merge_strategy}"}

        merged_result = self._merge_outputs(source_nodes, merge_strategy, context)
        if "error" in merged_result:
            return {"status": "error", "message": merged_result["error"]}

        return {
            "status": "success",
            "message": "Merge operation completed successfully",
            "result": merged_result
        }

    def _merge_outputs(self, source_nodes, strategy, context):
        """
        Merges outputs from the given source nodes based on the specified strategy.
        """
        outputs = []
        key_based_result = {}

        for node in source_nodes:
            result = context.get(node)
            if not result:
                logger.warning(f"No output found for node '{node}'. Skipping.")
                continue

            outputs.append(result)

            if strategy == "key_based":
                if not isinstance(result, dict):
                    return {"error": f"Node '{node}' output must be a dictionary for key-based merging"}
                for key, value in result.items():
                    key_based_result.setdefault(key, []).append(value)

        if strategy == "concatenate":
            return outputs  # List of results
        elif strategy == "aggregate":
            return {"aggregated_data": outputs}  # Wrap in a single key
        elif strategy == "key_based":
            return key_based_result

        return {"error": "Unknown merge strategy"}

if __name__ == "__main__":
    # Example usage
    merge_node = MergeNode()
    test_data = {
        "source_nodes": ["node1", "node2", "node3"],
        "merge_strategy": "key_based",
        "input": {
            "node1": {"key1": "value1", "key2": "value2"},
            "node2": {"key1": "value3", "key2": "value4"},
            "node3": {"key3": "value5"}
        }
    }
    result = merge_node.execute(test_data)
    print(json.dumps(result, indent=2))
