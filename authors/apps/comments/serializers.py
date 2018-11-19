from rest_framework import serializers
from rest_framework.exceptions import APIException
from authors.apps.comments.models import Comments, CommentsLikeDislike
from authors.apps.authentication.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        read_only_fields = ["author", "article"]
        exclude = ("article",)

    def to_representation(self, data):
        """ Change the default layout of the object """
        comment = super(CommentSerializer, self).to_representation(data)
        if User.objects.filter(pk=comment["author"]).exists():
            user_details = User.objects.get(pk=comment["author"])
            comment["author"] = {
                "id": user_details.id,
                "email": user_details.email,
                "username": user_details.username,
            }
        comments = comment
        if len(comments) > 2:
            return comments
        else:
            return {"comment": comments}


class CommentLikesDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsLikeDislike
        fields = '__all__'
        read_only_fields = ['comment', 'users']
        # exclude = ('users',)

    def to_representation(self, data):
        ''' Change the way the comment dislike is viewed '''
        commentlike = super(CommentLikesDislikeSerializer,
                            self).to_representation(data)
        if User.objects.filter(pk=commentlike['users']).exists():
            print(User.objects.filter(pk=commentlike['users']))
            user = User.objects.get(pk=commentlike['users'])
            commentlike['users'] = {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        commentlike_details = commentlike
        return commentlike_details
