"""
    auth_app API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import unittest

from auth_client.api.user_api import UserApi  # noqa: E501


class TestUserApi(unittest.TestCase):
    """UserApi unit test stubs"""

    def setUp(self):
        self.api = UserApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_auth_users_v1_change_password_post(self):
        """Test case for auth_users_v1_change_password_post

        Change Password  # noqa: E501
        """
        pass

    def test_auth_users_v1_login_history_get(self):
        """Test case for auth_users_v1_login_history_get

        Login History  # noqa: E501
        """
        pass

    def test_auth_users_v1_login_post(self):
        """Test case for auth_users_v1_login_post

        Login  # noqa: E501
        """
        pass

    def test_auth_users_v1_logout_delete(self):
        """Test case for auth_users_v1_logout_delete

        Logout  # noqa: E501
        """
        pass

    def test_auth_users_v1_refresh_post(self):
        """Test case for auth_users_v1_refresh_post

        Refresh  # noqa: E501
        """
        pass

    def test_auth_users_v1_register_post(self):
        """Test case for auth_users_v1_register_post

        Register  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
