from rest_framework import generics
from rest_framework import permissions
from authors.apps.articles.models import Article
from rest_framework import response
from .models import Comments
from rest_framework import status
from .serializers import CommentSerializer
from .renders import CommentsRenderer
from .permissions import IsOwnerOrReadOnly
from authors.apps.authentication.models import User


class CommentList(generics.ListCreateAPIView):

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = (CommentsRenderer,)
    lookup_field = "slug"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        comment = request.data.get("comment", {})
        serializer = CommentList.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        user = request.user
        slug = kwargs["slug"]
        articles = Article.objects.filter(slug=slug).first()
        current_user = User.objects.filter(email=user).first()
        serializer.save(author=current_user, article=articles)
        return response.Response(
            {"message": "comment created ", "comment": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """ Return a view using the slug """
        slug = self.kwargs["slug"]
        _id = Article.objects.filter(slug=slug).first().id
        comments = Comments.objects.filter(article_id=_id).all()
        return comments


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_fields = ["pk", "slug"]
