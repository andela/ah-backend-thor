from authors.apps.authentication.models import User
from authors.apps.core.utils.utils import Utils
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer

from rest_framework import generics, permissions, status

from rest_framework.response import Response


class FavoriteArticleView(generics.CreateAPIView):
    permission_class = permissions.IsAuthenticated

    def post(self, request, *args, **kwargs):
        util = Utils()
        author_id = util.get_token(request)
        slug = kwargs["slug"]
        user = author_id
        article = Article.objects.filter(slug=slug).first()
        if article is not None:
            article.fav_user.add(user)
            artile_count = article.fav_user.all().count()
            Article.objects.filter(slug=slug).update(
                favorites_count=artile_count)

            article_id = article.id
            article2 = Article.objects.filter(id=article_id).first()
            article2.favorited = True
            article_data = ArticleSerializer(article2).data
            return Response(article_data)

        return Response({"message": "favorited article doesnot exist"})


class DeleteFavoriteView(generics.DestroyAPIView):
    permission_class = permissions.IsAuthenticated

    def delete(self, request, *args, **kwargs):
        util = Utils()
        author_id = util.get_token(request)
        slug = kwargs["slug"]
        user = author_id
        article = Article.objects.filter(slug=slug).first()
        if article is not None:
            article.fav_user.remove(user)
            artile_count = article.fav_user.all().count()
            Article.objects.filter(slug=slug).update(
                favorites_count=artile_count)

            article_id = article.id
            article2 = Article.objects.filter(id=article_id).first()
            article_data = ArticleSerializer(article2).data
            return Response(article_data)
        return Response({"message": "favorited article doesnot exits"})
