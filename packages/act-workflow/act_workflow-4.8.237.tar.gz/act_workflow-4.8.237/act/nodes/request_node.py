from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType
from typing import Dict, Any, Optional
import aiohttp
import asyncio
import json
from urllib.parse import urlparse

class HTTPRequestNode(BaseNode):
    def get_schema(self) -> NodeSchema:
        return NodeSchema(
            node_type='http_request',
            version='1.0.0',
            description='Makes HTTP requests to external endpoints with configurable parameters',
            parameters=[
                NodeParameter(
                    name='url',
                    type=NodeParameterType.STRING,
                    description='The URL to send the request to',
                    required=True
                ),
                NodeParameter(
                    name='method',
                    type=NodeParameterType.STRING,
                    description='HTTP method to use',
                    required=False,
                    default='GET',
                    enum=['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
                ),
                NodeParameter(
                    name='headers',
                    type=NodeParameterType.OBJECT,
                    description='HTTP headers to include in the request',
                    required=False,
                    default={}
                ),
                NodeParameter(
                    name='body',
                    type=NodeParameterType.OBJECT,
                    description='Request body (for POST/PUT/PATCH requests)',
                    required=False,
                    default=None
                ),
                NodeParameter(
                    name='timeout',
                    type=NodeParameterType.NUMBER,
                    description='Request timeout in seconds',
                    required=False,
                    default=30
                ),
                NodeParameter(
                    name='verify_ssl',
                    type=NodeParameterType.BOOLEAN,
                    description='Whether to verify SSL certificates',
                    required=False,
                    default=True
                )
            ],
            outputs={
                'status_code': NodeParameterType.NUMBER,
                'headers': NodeParameterType.OBJECT,
                'body': NodeParameterType.OBJECT,
                'error': NodeParameterType.STRING
            }
        )

    def validate_url(self, url: str) -> bool:
        """Validate URL format and scheme."""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate input data against schema
            validated_data = self.validate_schema(node_data)
            
            url = validated_data['url']
            if not self.validate_url(url):
                raise ValueError(f"Invalid URL format: {url}")

            method = validated_data.get('method', 'GET')
            headers = validated_data.get('headers', {})
            body = validated_data.get('body')
            timeout = validated_data.get('timeout', 30)
            verify_ssl = validated_data.get('verify_ssl', True)

            # Convert timeout to aiohttp format
            timeout_obj = aiohttp.ClientTimeout(total=timeout)

            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if body else None,
                    ssl=verify_ssl
                ) as response:
                    # Read response body
                    try:
                        response_body = await response.json()
                    except (json.JSONDecodeError, aiohttp.ContentTypeError):
                        # If not JSON, get raw text
                        response_body = await response.text()

                    return {
                        'status': 'success',
                        'result': {
                            'status_code': response.status,
                            'headers': dict(response.headers),
                            'body': response_body,
                            'error': None
                        }
                    }

        except aiohttp.ClientError as e:
            return self.handle_error(
                e, 
                context=f'HTTP request failed: {str(e)}',
                status_code=getattr(e, 'status', 500)
            )
        except Exception as e:
            return self.handle_error(e, context='HTTPRequestNode execution')

    def handle_error(self, error: Exception, context: str, status_code: int = 500) -> Dict[str, Any]:
        """Enhanced error handling with status code support."""
        return {
            'status': 'error',
            'result': {
                'status_code': status_code,
                'headers': {},
                'body': None,
                'error': f"{context}: {str(error)}"
            }
        }


if __name__ == "__main__":
    async def test_node():
        node = HTTPRequestNode()
        
        # Test successful GET request
        test_data = {
            'url': 'https://jsonplaceholder.typicode.com/posts/1',
            'method': 'GET'
        }
        result = await node.execute(test_data)
        print("GET Test Result:", json.dumps(result, indent=2))

        # Test POST request
        test_post_data = {
            'url': 'https://jsonplaceholder.typicode.com/posts',
            'method': 'POST',
            'headers': {'Content-Type': 'application/json'},
            'body': {
                'title': 'Test Post',
                'body': 'Test Body',
                'userId': 1
            }
        }
        result = await node.execute(test_post_data)
        print("\nPOST Test Result:", json.dumps(result, indent=2))

        # Test invalid URL
        test_invalid_data = {
            'url': 'invalid-url',
            'method': 'GET'
        }
        result = await node.execute(test_invalid_data)
        print("\nInvalid URL Test Result:", json.dumps(result, indent=2))

    asyncio.run(test_node())