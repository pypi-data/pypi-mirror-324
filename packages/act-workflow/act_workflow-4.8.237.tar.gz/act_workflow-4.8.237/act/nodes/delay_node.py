import time
import logging
from typing import Dict, Any
from .base_node_prod import BaseNode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DelayNode(BaseNode):
    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the delay operation.
        """
        try:
            logger.info("Executing DelayNode...")
            logger.debug(f"Node data received: {node_data}")

            # Get delay time parameter
            delay_time = node_data.get("delay_time")
            if isinstance(delay_time, str):
                delay_time = delay_time.strip('"\'')

            # Convert to integer and validate
            try:
                seconds = int(delay_time)
                if seconds < 0:
                    return {
                        "status": "error",
                        "message": "delay_time must be a positive integer"
                    }
            except (ValueError, TypeError):
                return {
                    "status": "error",
                    "message": f"Invalid delay_time value: {delay_time}"
                }

            # Get input from previous node
            input_data = node_data.get("input", {})
            
            logger.info(f"Starting delay of {seconds} seconds")
            time.sleep(seconds)  # Use synchronous sleep
            logger.info(f"Completed delay of {seconds} seconds")

            return {
                "status": "success",
                "message": f"Successfully delayed execution for {seconds} seconds",
                "result": {
                    "delay_time": seconds,
                    "input_preserved": input_data.get("result", {})
                }
            }

        except Exception as e:
            logger.error(f"Error in DelayNode execution: {str(e)}")
            return {
                "status": "error",
                "message": f"Error during delay execution: {str(e)}"
            }