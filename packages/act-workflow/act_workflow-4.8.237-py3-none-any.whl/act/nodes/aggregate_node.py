import json
import logging
from typing import Dict, Any, List
from .base_node_prod import BaseNode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class AggregateNode(BaseNode):
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the AggregateNode logic to aggregate data from multiple fields.
        """
        try:
            logger.info("Executing AggregateNode...")
            logger.debug(f"Node data received: {node_data}")

            # Get and clean input parameters
            input_data = node_data.get("input_data", [])
            aggregate_strategy = str(node_data.get("aggregate_strategy", "")).strip('"')
            output_field = str(node_data.get("output_field", "")).strip('"')

            # Handle previous node's input
            previous_input = node_data.get("input", {})
            if previous_input and isinstance(previous_input, dict):
                if "result" in previous_input:
                    # Use the result from the previous node as input data
                    input_data = [previous_input.get("result", {})]
                    logger.info(f"Using previous node result as input: {input_data}")

            # Ensure input_data is a list
            if not isinstance(input_data, list):
                try:
                    # Try parsing if it's a string representation
                    if isinstance(input_data, str):
                        input_data = json.loads(input_data.replace("'", '"'))
                except json.JSONDecodeError:
                    # If parsing fails, create a single-item list with the input
                    if previous_input:
                        input_data = [previous_input.get("result", {})]
                    else:
                        input_data = []

            # Validate the parameters
            if not input_data:
                return {
                    "status": "error",
                    "message": "No input data available for aggregation"
                }

            if not aggregate_strategy:
                aggregate_strategy = "merge"  # Default strategy

            if not output_field:
                output_field = "aggregated_result"  # Default output field

            # Perform aggregation based on strategy
            if aggregate_strategy == "merge":
                result = self._merge_data(input_data)
            elif aggregate_strategy == "concat":
                result = self._concat_data(input_data)
            elif aggregate_strategy == "sum":
                result = self._sum_data(input_data)
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported aggregate strategy: {aggregate_strategy}"
                }

            logger.info(f"Aggregation completed with strategy: {aggregate_strategy}")
            return {
                "status": "success",
                "message": "Data aggregated successfully",
                "result": {
                    output_field: result
                }
            }

        except Exception as e:
            logger.error(f"Error in AggregateNode execution: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def _merge_data(self, data_list: List[Any]) -> Dict:
        """Merge dictionaries in the data list."""
        result = {}
        for item in data_list:
            if isinstance(item, dict):
                self._deep_update(result, item)
        return result

    def _deep_update(self, target: Dict, source: Dict) -> None:
        """Recursively update target dict with source dict."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def _concat_data(self, data_list: List[Any]) -> List:
        """Concatenate lists or items in the data list."""
        result = []
        for item in data_list:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    def _sum_data(self, data_list: List[Any]) -> float:
        """Sum numeric values in the data list."""
        total = 0
        for item in data_list:
            if isinstance(item, (int, float)):
                total += item
            elif isinstance(item, dict):
                total += sum(v for v in item.values() if isinstance(v, (int, float)))
        return total

    def _extract_numeric_values(self, data: Any) -> List[float]:
        """Recursively extract numeric values from nested structures."""
        values = []
        if isinstance(data, (int, float)):
            values.append(float(data))
        elif isinstance(data, dict):
            for value in data.values():
                values.extend(self._extract_numeric_values(value))
        elif isinstance(data, list):
            for item in data:
                values.extend(self._extract_numeric_values(item))
        return values