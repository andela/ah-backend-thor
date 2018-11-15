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
        self.comments_url = "/api/comments/articles/how_do_i_write_good_code/comments/"
        self.create_comment_like_url = '/api/comments/1/like'
        self.comment_likes_url = '/api/comments/1/like'

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

        self.comment = {"comment": {"body": "Code is fun to write"}}

    def test__user_can_like_dislike_a_comment(self):
        """ Creates a comment like to a user comment """
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
        comment_post_response = self.client.post(
            self.comments_url, self.comment, **headers, format="json"
        )
        self.assertEqual(comment_post_response.status_code, 201)

        comment_get_response = self.client.get(
            self.comments_url, **headers, format="json"
        )
        self.assertEqual(comment_get_response.status_code, 200)
        like_comment_response = self.client.post(
            self.create_comment_like_url, **headers, format='json')
        self.assertEqual(like_comment_response.status_code, 200)
        self.assertIn("Comment liked", like_comment_response.data['message'])
        comment_likes = self.client.get(
            self.comment_likes_url, **headers, format='json')
        self.assertIn('like', comment_likes.data['likes'][0])
