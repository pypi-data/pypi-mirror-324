import json
import logging
from .base_node_prod import BaseNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class JoinNode(BaseNode):
    def execute(self, node_data):
        """
        Joins multiple inputs into a single list or string.
        """
        logger.info("Executing JoinNode...")

        # Validate required parameters
        input_data = node_data.get("input_data")
        join_type = node_data.get("join_type", "list").lower()
        delimiter = node_data.get("delimiter", ", ")
        output_field = node_data.get("output_field", "joined_data")

        if not input_data or not isinstance(input_data, list):
            return {"status": "error", "message": "'input_data' must be a list"}
        if join_type not in ["list", "string"]:
            return {"status": "error", "message": "'join_type' must be 'list' or 'string'"}

        try:
            joined_data = self._join_data(input_data, join_type, delimiter)
            return {
                "status": "success",
                "message": "Joining completed successfully",
                "result": {output_field: joined_data}
            }
        except Exception as e:
            logger.error(f"Error during joining: {e}")
            return {"status": "error", "message": str(e)}

    def _join_data(self, data, join_type, delimiter):
        """
        Joins the data based on the specified type and delimiter.
        """
        if join_type == "list":
            # Flatten lists into a single list
            joined_list = []
            for item in data:
                if isinstance(item, list):
                    joined_list.extend(item)
                else:
                    joined_list.append(item)
            return joined_list

        elif join_type == "string":
            # Concatenate strings with the specified delimiter
            return delimiter.join(map(str, data))

        raise ValueError("Unsupported join type")

if __name__ == "__main__":
    # Example usage
    join_node = JoinNode()
    test_data = {
        "input_data": [
            ["John", "Jane"],
            ["Doe", "Smith"],
            "Anderson"
        ],
        "join_type": "string",
        "delimiter": " | ",
        "output_field": "joined_results"
    }
    result = join_node.execute(test_data)
    print(json.dumps(result, indent=2))
