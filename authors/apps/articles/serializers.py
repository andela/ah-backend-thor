from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import Article, Rate, LikeArticle
from authors.apps.authentication.models import User
from .validation import Validator
from rest_framework.validators import UniqueTogetherValidator
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


# def get_user(logged_in_user, author, article):
#     if logged_in_user != author:
#         del article

class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tag_list = TagListSerializerField()

    class Meta:
        model = Article
        # fields = '__all__'
        exclude = ("fav_user", "bookmarks")

    def to_representation(self, data):
        ''' Show article's actual details'''
        article_details = super(
            ArticleSerializer, self).to_representation(data)
        if User.objects.filter(pk=int(article_details['author'])).exists():
            user_details = User.objects.get(
                pk=int(article_details['author']))
            article_details['author'] = {
                'id': user_details.id,
                'email': user_details.email,
                'username': user_details.username
            }
            if self.context.get('author_id') != user_details.id:
                del article_details['read_stats']
            # get_user(self.context.get('author_id'),
            #          user_details.id, article_details['read_stats'])
            return article_details
        return APIException({
            'error': 'User does not exist!'
        })
    

    def validate(self, data):

        validator = Validator
        title = data.get('title', None)
        description = data.get('description', None)
        body = data.get('body', None)
        tags = data.get('tag_list', None)

        validator.letter_starts('title', title)
        validator.letter_starts('description', description)
        validator.letter_starts('body', body)

        for tag in tags:
            validator.letter_starts('tag', tag)
        return data


class ArticleUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tag_list = TagListSerializerField()

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description',
                  'body', 'tag_list', 'image_url', 'audio_url']



class ArticleUpdateStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['read_stats']

class RateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        rate = data.get('rate')
        user = data.get('user')
        article = data.get('article')

        if rate is None:
            raise serializers.ValidationError(
                'A rating is required to vote for an article.'
            )
        if user is None:
            raise serializers.ValidationError(
                'Authentication credentials are missing'
            )
        if article is None:
            raise serializers.ValidationError(
                'The article to which you are voting is missing'
            )
        return {"rate": rate, "user": user, "article": article}

    class Meta:
        model = Rate
        fields = ('id', 'article', 'rate', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=Rate.objects.all(),
                fields=('user', 'article')
            )
        ]

    def create(self, validated_data):
        rate = Rate.objects.create(**validated_data)
        return rate

class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeArticle
        fields = '__all__'

    def to_representation(self, data):
        '''Show like details'''
        like_details = super(ArticleLikeSerializer, self).to_representation(data)
        if User.objects.filter(pk=like_details['user']).exists():
            user_details = User.objects.get(pk=like_details['user'])
            like_details['user'] = user_details.username
            return like_details
        return APIException({
            'error': 'User does not exist'
        })

class ArticleLikesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeArticle
        fields = ['like_status']
