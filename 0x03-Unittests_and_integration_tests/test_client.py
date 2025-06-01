from unittest import TestCase
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock

class TestGithubOrgClient(TestCase):
    """Test class for GithubOrgClient"""
    
    @patch.object(GithubOrgClient, "org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test method for public_repos_url property"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        mock_org.return_value = test_payload
        
        client = GithubOrgClient('test-org')
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/test-org/repos")
        mock_org.assert_called_once()
