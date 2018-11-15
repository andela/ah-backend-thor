from rest_framework import generics, permissions, status
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.core.utils.utils import Utils
from authors.apps.articles.serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class GetBookMarksView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get(self, request, *args):
        util = Utils()
        user = util.get_token(request)
        user_obj = User.objects.get(id=user)
        queryset = Article.objects.filter(bookmarks__id=user)
        if queryset:
            data = []
            for obj in queryset:
                article = Article.objects.get(id=obj.id)
                article_data = ArticleSerializer(article).data
                data.append(article_data)
            return Response(data)
        return Response({"message": "No Articles exist"})


class CreateBookMarksView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        util = Utils()
        user = util.get_token(request)
        slug = kwargs["slug"]
        article = Article.objects.filter(slug=slug).first()
        if article:
            article.bookmarks.add(user)
            article_id = article.id
            article2 = Article.objects.filter(id=article_id).first()
            article_data = ArticleSerializer(article2).data
            return Response({"bookmarked": article_data})

        return Response({"message": "Article doesnot exist"})


class DeleteBookMarkView(generics.DestroyAPIView):
    permission_class = permissions.IsAuthenticated

    def delete(self, request, *args, **kwargs):
        util = Utils()
        author_id = util.get_token(request)
        slug = kwargs["slug"]
        user = author_id
        try:
            article = Article.objects.filter(
                slug=slug, bookmarks__id=user).first()
            user_in_bookmarks = Article.objects.filter(
                bookmarks__id=user, article_id=article.id)
            if user_in_bookmarks is not None:
                article.bookmarks.remove(user)
                article_id = article.id
                article2 = Article.objects.filter(id=article_id).first()
                article_data = ArticleSerializer(article2).data
                return Response(article_data)
            return Response({"message for user": "user for bookmarked article doesnot exits"})
        except:
            return Response({"article bookmark message": "bookmarked article doesnot exits"})
