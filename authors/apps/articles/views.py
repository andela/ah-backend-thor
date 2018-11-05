import re
import time

import jwt
from authors.apps.authentication.models import User
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Article
from .renderers import ArticlesRenderer
from .serializers import ArticleSerializer


class ArticlesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permission_class = permissions.IsAuthenticatedOrReadOnly

    def create(self, request, *args, **kwargs):

        article = request.data.get('article')
        
        title = article['title']
        description = article['description']
        body = article['body']
        tags = article['tag_list']
        imageUrl = article['image_url']
        audioUrl = article['image_url']
        try:
            token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
            author = payload['id']
        except Exception as exception:
            raise APIException({
                'error': f'Login Token required. System error: {str(exception)}'
            })
        # create unique slug with only alphanumeric characters and dashes for spaces
        slug = ''
        for word in re.split(r'(.)', title.strip().lower()):
            if word.isalnum():
                slug += word
            elif word.isspace():
                slug += '_'

        # make slug unique with timestamp if slug already eists
        if Article.objects.filter(slug=slug).exists():
            slug += str(time.time()).replace('.', '')

        article = {
            'slug': slug,
            'title': title,
            'description': description,
            'body': body,
            'tag_list': tags,
            'image_url': imageUrl,
            'audio_url': audioUrl,
            'author': author
        }
        
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateArticleByIdApiView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'pk'


class GetArticleBySlugApiView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permissiion_classes = (permissions.AllowAny, )
    lookup_field = 'slug'

    # def put(self, request, *args, **kwargs):
    #     article = Article.objects.get(id=kwargs['pk'])
    #     article_ = request.data.get('article')

    #     try:
    #         token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
    #         payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
    #         author = payload['id']
    #     except Exception as exception:
    #         raise APIException({
    #             'error': f'Login Token required. System error: {str(exception)}'
    #         })
    #     # create unique slug with only alphanumeric characters and dashes for spaces
    #     slug = ''
    #     for word in re.split(r'(.)', article.title.strip().lower()):
    #         if word.isalnum():
    #             slug += word
    #         elif word.isspace():
    #             slug += '_'

    #     # make slug unique with timestamp if slug already eists
    #     if Article.objects.filter(slug=slug).exists():
    #         slug += str(time.time()).replace('.', '')

    #     new_article = {
    #         'slug': article.slug ,
    #         'title': article.title or article_['title'] ,
    #         'description': article.description or article_['description'],
    #         'body': article.body or article_['body'] ,
    #         'tag_list': article.tag_list or article_['tags'] ,
    #         'image_url': article.image_url or article_['image_url'] ,
    #         'audio_url': article.audio_url or  article_['audio_url'] ,
    #         'author': author
    #     }
        
    #     serializer = self.serializer_class(data=article)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.update( article, new_article)
    #     # serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

