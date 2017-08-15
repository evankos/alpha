import unittest

from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from backdoor.CustomAssertions import CustomAssertions
from rest_framework import status



class AuthTests(TestCase, CustomAssertions):
    def setUp(self):
        self.unauthorized_client = Client()

        self.normalUser = User.objects.create_user('normal', 'normie@test.com', 'pass')
        self.adminUser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminUser.is_staff = True
        self.normalUser.save()
        self.adminUser.save()

        self.normalUserToken = Token.objects.get(user=self.normalUser)
        self.adminUserToken = Token.objects.get(user=self.adminUser)

        self.basic_auth_client_normal = Client(HTTP_AUTHORIZATION='Basic bm9ybWFsOnBhc3M=')
        self.token_auth_client_normal = Client(HTTP_AUTHORIZATION='Token %s' % self.normalUserToken.key)
        self.basic_auth_client_admin = Client(HTTP_AUTHORIZATION='Basic YWRtaW46cGFzcw==')
        self.token_auth_client_admin = Client(HTTP_AUTHORIZATION='Token %s' % self.adminUserToken.key)

    def test_auth_token_retrieved(self):
        """Test that we can retrieve the authentication token"""
        response = self.unauthorized_client.post('/api-token-auth/', {'username': 'normal', 'password': 'pass'})
        self.assertDictHasKey(response.json(), 'token')
        self.assertEqual(self.normalUserToken.key,response.json()['token'])

    def test_IsAuthenticated_enforced(self):
        """Test that u need to be logged in to access protected views"""
        response = self.unauthorized_client.get('/api/groups/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,"No credential call succeeded, that is bad.")
        response = self.basic_auth_client_normal.get('/api/groups/', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Basic Authentication failed")
        response = self.token_auth_client_normal.get('/api/groups/', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Token Authentication failed")

    def test_IsAdminUser_enforced(self):
        """Test that u need to be admin to access protected views"""
        response = self.unauthorized_client.get('/api/users/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,"No credential call succeeded, that is bad.")
        response = self.basic_auth_client_normal.get('/api/users/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "Basic Authentication failed")
        response = self.token_auth_client_normal.get('/api/users/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "Token Authentication failed")

        response = self.token_auth_client_admin.get('/api/users/', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Token Authentication failed")
        response = self.basic_auth_client_admin.get('/api/users/', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Basic Authentication failed")








if __name__ == '__main__':
    unittest.main()
