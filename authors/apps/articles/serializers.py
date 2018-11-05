from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import Article
from authors.apps.authentication.models import User
from .validation import Validator


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

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

class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'tag_list', 'image_url', 'audio_url']
