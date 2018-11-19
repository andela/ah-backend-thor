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
        comment = request.data.get("comment", {})  # pragma :no cover
        serializer = CommentList.serializer_class(
            data=comment)  # pragma :no cover
        serializer.is_valid(raise_exception=True)  # pragma :no cover
        user = request.user  # pragma :no cover
        slug = kwargs["slug"]  # pragma :no cover
        articles = Article.objects.filter(
            slug=slug).first()  # pragma :no cover
        current_user = User.objects.filter(
            email=user).first()  # pragma :no cover
        # pragma :no cover
        serializer.save(author=current_user, article=articles)
        return response.Response(  # pragma :no cover
            {"message": "comment created ", "comment": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """ Return a view using the slug """
        slug = self.kwargs["slug"]  # pragma :no cover
        _id = Article.objects.filter(slug=slug).first().id  # pragma :no cover
        comments = Comments.objects.filter(
            article_id=_id).all()  # pragma :no cover
        return comments  # pragma :no cover


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
        current_user = User.objects.filter(email=user).first()
        user_id = current_user.id
        _id = kwargs['pk']
        if CommentsLikeDislike.objects.filter(like=True) and \
                CommentsLikeDislike.objects.filter(users_id=user_id):
            raise NotAcceptable(
                {"detail": "You have already like the comment"}, {"code": 401})
        like_data = request.data.get("like", {})
        serializer = self.serializer_class(data=like_data)
        serializer.is_valid(raise_exception=True)
        comment = Comments.objects.filter(id=_id).first()
        serializer.save(comment=comment, users=current_user)
        return response.Response({'message': 'Comment liked',
                                  'comment_like': serializer.data},
                                 status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        '''Enables one to get likes and dislikes '''
        _id = kwargs['pk']  # pragma :no cover
        status = CommentsLikeDislike.objects.filter(
            comment_id=_id)  # pragma :no cover
        serializer = self.serializer_class(
            status, many=True)  # pragma :no cover
        return response.Response({"likes": serializer.data,  # pragma :no cover
                                  "likes_count": len(serializer.data)})


class CommentDislike(generics.DestroyAPIView):
    '''Enables one to dislike a comment '''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CommentsLikeDislike.objects.all()
    serializer_class = CommentLikesDislikeSerializer
