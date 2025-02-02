import json
import logging
import requests
import base64
from typing import Dict, Any, Optional
from base_node_prod import BaseNode, NodeSchema, NodeParameter, NodeParameterType

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GitHubNode(BaseNode):
    """GitHub API Node with enhanced schema validation."""

    def get_schema(self) -> NodeSchema:
        """Define the schema for GitHub node."""
        return NodeSchema(
            node_type="github",
            version="1.0.0",
            description="Node for interacting with GitHub API",
            parameters=[
                NodeParameter(
                    name="action",
                    type=NodeParameterType.STRING,
                    description="GitHub API action to perform",
                    required=True,
                    enum=[
                        "list_repositories",
                        "get_repository",
                        "create_repository",
                        "update_repository",
                        "delete_repository",
                        "list_issues",
                        "create_issue",
                        "get_issue",
                        "create_file",
                        "update_file",
                        "delete_file",
                        "list_pulls",
                        "create_pull",
                        "merge_pull"
                    ]
                ),
                NodeParameter(
                    name="token",
                    type=NodeParameterType.STRING,
                    description="GitHub Personal Access Token",
                    required=True
                ),
                NodeParameter(
                    name="owner",
                    type=NodeParameterType.STRING,
                    description="Repository owner (username or organization)",
                    required=True
                ),
                NodeParameter(
                    name="repo",
                    type=NodeParameterType.STRING,
                    description="Repository name",
                    required=True
                ),
                NodeParameter(
                    name="ref",
                    type=NodeParameterType.STRING,
                    description="Git reference (branch, tag, or commit SHA)",
                    required=False,
                    default="main"
                ),
                NodeParameter(
                    name="file_path",
                    type=NodeParameterType.STRING,
                    description="Path to file in repository",
                    required=False
                ),
                NodeParameter(
                    name="content",
                    type=NodeParameterType.STRING,
                    description="Content for file operations",
                    required=False
                ),
                NodeParameter(
                    name="commit_message",
                    type=NodeParameterType.STRING,
                    description="Commit message for file operations",
                    required=False,
                    default="Update from workflow"
                ),
                NodeParameter(
                    name="title",
                    type=NodeParameterType.STRING,
                    description="Title for issues and pull requests",
                    required=False
                ),
                NodeParameter(
                    name="body",
                    type=NodeParameterType.STRING,
                    description="Body for issues and pull requests",
                    required=False
                ),
                NodeParameter(
                    name="sha",
                    type=NodeParameterType.STRING,
                    description="File SHA for update/delete operations",
                    required=False
                )
            ],
            outputs={
                "status_code": NodeParameterType.NUMBER,
                "headers": NodeParameterType.OBJECT,
                "body": NodeParameterType.OBJECT
            }
        )

    def _build_github_url(self, action: str, owner: str, repo: str, file_path: Optional[str] = None) -> str:
        """Build GitHub API URL based on action."""
        base_url = "https://api.github.com"

        if action == "list_repositories":
            return f"{base_url}/users/{owner}/repos"
        elif action == "create_repository":
            return f"{base_url}/user/repos"
        elif action in ["get_repository", "update_repository", "delete_repository"]:
            return f"{base_url}/repos/{owner}/{repo}"
        elif action in ["list_issues", "create_issue", "get_issue"]:
            return f"{base_url}/repos/{owner}/{repo}/issues"
        elif action in ["list_pulls", "create_pull", "merge_pull"]:
            return f"{base_url}/repos/{owner}/{repo}/pulls"
        elif action in ["create_file", "update_file", "delete_file"]:
            # file_path is required for file operations
            return f"{base_url}/repos/{owner}/{repo}/contents/{file_path}"

        raise ValueError(f"Unsupported action: {action}")

    def _get_request_method(self, action: str) -> str:
        """Determine HTTP method based on action."""
        method_map = {
            "list_repositories": "GET",
            "get_repository": "GET",
            "create_repository": "POST",
            "update_repository": "PATCH",
            "delete_repository": "DELETE",
            "list_issues": "GET",
            "create_issue": "POST",
            "get_issue": "GET",
            "list_pulls": "GET",
            "create_pull": "POST",
            "merge_pull": "PUT",
            "create_file": "PUT",
            "update_file": "PUT",
            "delete_file": "DELETE"
        }
        return method_map.get(action, "GET")

    def _prepare_request_body(self, action: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare request body based on action."""
        if action == "create_repository":
            return {
                "name": node_data["repo"],
                "description": node_data.get("description", ""),
                "private": node_data.get("private", False)
            }
        elif action == "create_issue":
            return {
                "title": node_data["title"],
                "body": node_data.get("body", ""),
                "labels": node_data.get("labels", [])
            }
        elif action == "create_pull":
            return {
                "title": node_data["title"],
                "body": node_data.get("body", ""),
                "head": node_data.get("head", "main"),
                "base": node_data.get("base", "main")
            }
        elif action == "create_file":
            # For create_file, we encode the content
            content = node_data.get("content", "")
            if isinstance(content, str):
                content = base64.b64encode(content.encode()).decode()
            return {
                "message": node_data.get("commit_message", "Add file"),
                "content": content,
                "branch": node_data.get("ref", "main")
            }
        elif action == "update_file":
            # Check for sha to prevent KeyError
            if "sha" not in node_data:
                raise ValueError("Missing required field: sha")
            content = node_data.get("content", "")
            if isinstance(content, str):
                content = base64.b64encode(content.encode()).decode()
            return {
                "message": node_data.get("commit_message", "Update file"),
                "content": content,
                "sha": node_data["sha"],
                "branch": node_data.get("ref", "main")
            }
        elif action == "delete_file":
            # Check for sha to prevent KeyError
            if "sha" not in node_data:
                raise ValueError("Missing required field: sha")
            return {
                "message": node_data.get("commit_message", "Delete file"),
                "sha": node_data["sha"],
                "branch": node_data.get("ref", "main")
            }

        return {}

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub API request."""
        try:
            logger.info("Executing GitHubNode...")

            # Basic required fields validation
            required_fields = ["action", "token", "owner", "repo"]
            for field in required_fields:
                if field not in node_data:
                    raise ValueError(f"Missing required field: {field}")

            action = node_data["action"]
            token = node_data["token"]
            owner = node_data["owner"]
            repo = node_data["repo"]
            file_path = node_data.get("file_path")

            # Additional validation for file operations
            if action in ["create_file", "update_file", "delete_file"]:
                if not file_path:
                    raise ValueError("file_path is required for file operations")

            # Build request URL and get method
            url = self._build_github_url(action, owner, repo, file_path)
            method = self._get_request_method(action)

            # Setup headers
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "GitHubNode/1.0.0"
            }

            # Prepare request body
            request_body = self._prepare_request_body(action, node_data)

            # Log request details (excluding sensitive data)
            safe_data = {k: v for k, v in node_data.items() if k not in ["token", "content"]}
            logger.info(f"Making GitHub API request: {method} {url}")
            logger.debug(f"Request data: {safe_data}")

            # Make the request
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=request_body if request_body else None
                )

                # Parse response
                response_data = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.json() if response.content else {}
                }

                # Return success or error based on status code
                if 200 <= response.status_code < 300:
                    return {
                        "status": "success",
                        "message": f"GitHub API request completed successfully",
                        "result": response_data
                    }
                else:
                    error_message = response_data["body"].get("message", "Unknown error")
                    return {
                        "status": "error",
                        "message": f"GitHub API request failed: {error_message}",
                        "result": response_data
                    }

            except requests.exceptions.RequestException as e:
                return self.handle_error(e, f"GitHub API request failed: {str(e)}")

        except Exception as e:
            return self.handle_error(e, "GitHubNode execution")


if __name__ == "__main__":
    # Test GitHubNode manually
    github_node = GitHubNode()

    # Example: create_file
    test_data = {
        "action": "create_file",
        "token": "your-github-token",
        "owner": "your-username",
        "repo": "your-repo",
        "file_path": "test/example.md",
        "content": "# Test Content\nThis is a test file.",
        "commit_message": "Add test file"
    }
    result = github_node.execute(test_data)
    print(json.dumps(result, indent=2))
