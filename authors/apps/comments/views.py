from rest_framework import generics
from rest_framework.exceptions import NotAcceptable
from rest_framework import permissions
from authors.apps.articles.models import Article
from rest_framework import response
from .models import Comments, CommentsLikeDislike
from rest_framework import status
from .serializers import CommentSerializer, CommentLikesDislikeSerializer
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


class CommentLike(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CommentsLikeDislike.objects.all()
    serializer_class = CommentLikesDislikeSerializer

    def post(self, request, *args, **kwargs):
        '''enables one to post a like  to a comment'''
        user = request.user
        _id = kwargs['pk']
        if CommentsLikeDislike.objects.filter(like=True) and CommentsLikeDislike.objects.filter(users_id=_id):
            raise NotAcceptable(
                {"detail": "You have already like the comment"}, {"code": 401})
        like_data = request.data.get("like", {})
        serializer = self.serializer_class(data=like_data)
        serializer.is_valid(raise_exception=True)
        comment = Comments.objects.filter(id=_id).first()
        current_user = User.objects.filter(email=user).first()
        serializer.save(comment=comment, users=current_user)
        return response.Response({'message': 'Comment liked',
                                  'comment_like': serializer.data},
                                 status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        '''Enables one to get likes and dislikes '''
        _id = kwargs['pk']
        status = CommentsLikeDislike.objects.filter(comment_id=_id)
        serializer = self.serializer_class(status, many=True)
        return response.Response({"likes": serializer.data})


class CommentDislike(generics.UpdateAPIView):
    '''Enables one to update a like or dislike '''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CommentsLikeDislike.objects.all()
    serializer_class = CommentLikesDislikeSerializer
