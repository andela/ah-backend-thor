from rest_framework.test import APIClient
from rest_framework.test import APITestCase
# from rest_framework.reverse import reverse


class TestEmailValidation(APITestCase):

    def setUp(self):
        self.email_verify_url = '/api/users/update/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQsImV4cCI6MTU0NjE3NTM5MX0.6NOhezpuI8Ib-YzJi1vM1DxypN3jCJ58fBC-YxphMxQ'
        self.client = APIClient()

    def test_email_verification(self):
        """test user email verification"""
        response = self.client.get(self.email_verify_url)
        # self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, 200,
                         'Expected Response1 Code 200, received {0} instead.'.format(response.status_code))
