import unittest
from unittest.mock import patch, MagicMock
from github_node import GitHubNode  # Adjust if your module path differs

class TestGitHubNode(unittest.TestCase):

    #
    # list_repositories
    #
    @patch("requests.request")
    def test_list_repositories_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"some": "data"}'
        mock_response.json.return_value = {"some": "data"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "list_repositories",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "ignored_for_list"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 200)
        self.assertEqual(result["result"]["body"], {"some": "data"})

    @patch("requests.request")
    def test_list_repositories_missing_owner(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "list_repositories",
            "token": "fake_token",
            # 'owner' missing
            "repo": "ignored_repo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: owner", result["message"])


    #
    # get_repository
    #
    @patch("requests.request")
    def test_get_repository_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"name": "testrepo"}'
        mock_response.json.return_value = {"name": "testrepo"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "get_repository",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["body"], {"name": "testrepo"})

    @patch("requests.request")
    def test_get_repository_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "get_repository",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # create_repository
    #
    @patch("requests.request")
    def test_create_repository_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"name": "newrepo"}'
        mock_response.json.return_value = {"name": "newrepo"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "create_repository",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "newrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 201)
        self.assertEqual(result["result"]["body"], {"name": "newrepo"})

    @patch("requests.request")
    def test_create_repository_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "create_repository",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # update_repository
    #
    @patch("requests.request")
    def test_update_repository_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"name": "updatedrepo"}'
        mock_response.json.return_value = {"name": "updatedrepo"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "update_repository",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "myrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 200)
        self.assertEqual(result["result"]["body"], {"name": "updatedrepo"})

    @patch("requests.request")
    def test_update_repository_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "update_repository",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # delete_repository
    #
    @patch("requests.request")
    def test_delete_repository_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = b''
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "delete_repository",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "oldrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 204)

    @patch("requests.request")
    def test_delete_repository_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "delete_repository",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # list_issues
    #
    @patch("requests.request")
    def test_list_issues_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"issues": []}'
        mock_response.json.return_value = {"issues": []}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "list_issues",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["body"], {"issues": []})

    @patch("requests.request")
    def test_list_issues_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "list_issues",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # create_issue
    #
    @patch("requests.request")
    def test_create_issue_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"title": "New Issue"}'
        mock_response.json.return_value = {"title": "New Issue"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "create_issue",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "title": "Issue Title"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 201)
        self.assertIn("title", result["result"]["body"])

    @patch("requests.request")
    def test_create_issue_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "create_issue",
            "token": "fake_token",
            "owner": "test_user",
            # missing 'repo'
            "title": "Issue Title"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # get_issue
    #
    @patch("requests.request")
    def test_get_issue_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"number": 123, "title": "Issue Title"}'
        mock_response.json.return_value = {"number": 123, "title": "Issue Title"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "get_issue",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo"
            # 'get_issue' typically would have an issue_number, but the node lumps them together
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 200)
        self.assertIn("title", result["result"]["body"])

    @patch("requests.request")
    def test_get_issue_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "get_issue",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # create_file
    #
    @patch("requests.request")
    def test_create_file_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"content": {"name": "README.md"}}'
        mock_response.json.return_value = {"content": {"name": "README.md"}}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "create_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "file_path": "README.md",
            "content": "# Hello World"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 201)
        self.assertIn("content", result["result"]["body"])

    @patch("requests.request")
    def test_create_file_missing_file_path(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "create_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            # missing 'file_path'
            "content": "# Hello World"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("file_path is required for file operations", result["message"])


    #
    # update_file
    #
    @patch("requests.request")
    def test_update_file_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"content": {"sha": "updated_sha"}}'
        mock_response.json.return_value = {"content": {"sha": "updated_sha"}}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "update_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "file_path": "README.md",
            "sha": "existing_sha",
            "content": "Updated Content"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("content", result["result"]["body"])

    @patch("requests.request")
    def test_update_file_missing_sha(self, mock_request):
        """Test error when 'sha' is missing for update_file."""
        node = GitHubNode()
        input_data = {
            "action": "update_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "file_path": "README.md",
            "content": "Updated Content"
            # missing 'sha'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: sha", result["message"])


    #
    # delete_file
    #
    @patch("requests.request")
    def test_delete_file_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{}'
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "delete_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "file_path": "README.md",
            "sha": "file_sha"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 200)

    @patch("requests.request")
    def test_delete_file_missing_sha(self, mock_request):
        """Test error when 'sha' is missing for delete_file."""
        node = GitHubNode()
        input_data = {
            "action": "delete_file",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "file_path": "README.md"
            # missing 'sha'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: sha", result["message"])


    #
    # list_pulls
    #
    @patch("requests.request")
    def test_list_pulls_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"pulls": []}'
        mock_response.json.return_value = {"pulls": []}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "list_pulls",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("pulls", result["result"]["body"])

    @patch("requests.request")
    def test_list_pulls_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "list_pulls",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # create_pull
    #
    @patch("requests.request")
    def test_create_pull_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"number": 1, "title": "New PR"}'
        mock_response.json.return_value = {"number": 1, "title": "New PR"}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "create_pull",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo",
            "title": "Add new feature",
            "body": "This is a new feature branch",
            "head": "feature-branch",
            "base": "main"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 201)
        self.assertIn("title", result["result"]["body"])

    @patch("requests.request")
    def test_create_pull_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "create_pull",
            "token": "fake_token",
            "owner": "test_user",
            # missing 'repo'
            "title": "Add new feature"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


    #
    # merge_pull
    #
    @patch("requests.request")
    def test_merge_pull_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"merged": true}'
        mock_response.json.return_value = {"merged": True}
        mock_request.return_value = mock_response

        node = GitHubNode()
        input_data = {
            "action": "merge_pull",
            "token": "fake_token",
            "owner": "test_user",
            "repo": "testrepo"
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["status_code"], 200)
        self.assertTrue(result["result"]["body"].get("merged"))

    @patch("requests.request")
    def test_merge_pull_missing_repo(self, mock_request):
        node = GitHubNode()
        input_data = {
            "action": "merge_pull",
            "token": "fake_token",
            "owner": "test_user"
            # missing 'repo'
        }
        result = node.execute(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing required field: repo", result["message"])


if __name__ == "__main__":
    unittest.main()
