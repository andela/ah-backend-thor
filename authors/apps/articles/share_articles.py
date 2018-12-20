import os
import jwt
from urllib.parse import quote
from .models import Article
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from django.conf import settings
from authors.apps.authentication.models import User
from authors.apps.core.utils.utils import Utils
from rest_framework.response import Response


class ShareArticleViaEmailAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"

    def post(self, request, *args, **kwargs):

        # decode token
        utils = Utils()
        user_id = utils.get_token(request)
        user_instance = User.objects.get(id=user_id)
        user_email = user_instance.email

        slug = self.kwargs["slug"]
        try:
            Article.objects.get(slug=slug)

            # get email from authentication to send to
            link = "https://ah-frontend-thor.herokuapp.com/display/{}".format(
                slug)

            from_email = os.getenv("EMAIL")
            to_email = [user_email]
            subject = "Article Link"
            message = "Read article using this link: " + link

            send_mail(subject, message, from_email,
                      to_email, fail_silently=False)

            return Response(
                {
                    "message": "Check your email for the link to article"
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response({
                "message": "Article not found"
            })


class ShareArticleViaFacebookAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        slug = self.kwargs["slug"]

        try:
            Article.objects.get(slug=slug)
            base_url = "https://www.facebook.com/sharer/sharer.php?u="
            heroku_link = "https://ah-frontend-thor.herokuapp.com/display/{}".format(
                slug
            )
            url_link = base_url + heroku_link

            return Response(
                {
                    "message": "Facebook link",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message": "Article not found"
            })


class ShareArticleViaTwitterAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"

    def post(self, request, *args, **kwargs):
        slug = self.kwargs[self.lookup_field]
        try:
            article_instance = Article.objects.get(slug=slug)

            data = quote(article_instance.title)
            base_url = "https://twitter.com/home?status="

            url_link = (
                base_url
                + "{0}%20https://ah-frontend-thor.herokuapp.com/display/{1}".format(
                    data, slug
                )
            )

            return Response(
                {
                    "message": "Twitter link",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message": "Article not found"
            })
