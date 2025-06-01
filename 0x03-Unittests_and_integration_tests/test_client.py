#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_client = GithubOrgClient(org_name)
        test_client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property"""
        expected_url = "https://api.github.com/orgs/test-org/repos"
        mock_org.return_value = {"repos_url": expected_url}
        client = GithubOrgClient("test-org")
        self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value='https://api.github.com/orgs/test-org/repos'
        ) as mock_public_repos_url:
            client = GithubOrgClient('test-org')
            repos = client.public_repos()

            self.assertEqual(repos, ['repo1', 'repo2'])
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()