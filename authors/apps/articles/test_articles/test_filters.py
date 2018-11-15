from rest_framework.test import APIClient, APITestCase
from authors.apps.authentication.models import User


class TestUserCommments(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""

        self.client = APIClient()
        self.register_url = "/api/users/"
        self.login_url = "/api/users/login/"
        self.articles_url = "/api/articles/"
        self.filters_url = "/api/articles/?title=How do i write good code"
        self.filters_tags_url = "/api/articles /?tags=coding"

        self.user = {
            "user": {
                "username": "dude",
                "email": "dude1@gmail.com",
                "password": "password",
            }
        }

        self.article = {
            "article": {
                "title": "How do i write good code",
                "description": "Ever wonder how people become good developers?",
                "body": "How long can I take to be a good programmer",
                "tag_list": ["coding", "python"],
                "image_url": "https://i.stack.imgur.com/xHWG8.jpg",
                "audio_url": "https://google.com/cpw.jpg",
            }
        }

    def test_user_can_get_an_article_based_filter(self):
        """ Creates a comment to a user question """
        response = self.client.post(
            self.register_url, self.user, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("User successfully Registered", response.data["message"])
        User.objects.filter(email="dude1@gmail.com").update(is_verified=True)
        response = self.client.post(self.login_url, self.user, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User successfully confirmed",
                      response.data["user_message"])
        token = response.data["user_token"]
        # self.assertIn("asasdas", token)
        headers = {"HTTP_AUTHORIZATION": "Token " + f"{token}"}
        # rev = self.client.get(self.get_user_url, **headers, format="json")
        article_response = self.client.post(
            self.articles_url, self.article, **headers, format="json"
        )
        self.assertEqual(article_response.status_code, 201)
        filter_response = self.client.get(
            self.filters_url, **headers, format="json")
        self.assertEqual(filter_response.status_code, 200)
        filter_tags_response = self.client.get(
            self.filters_tags_url, **headers, format="json")
        self.assertEqual(filter_response.status_code, 200)
