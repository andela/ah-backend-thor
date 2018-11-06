
import json
import re
import time

from authors.apps.authentication.models import User
from authors.apps.core.utils.utils import Utils
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Article
from .renderers import ArticlesRenderer
from .serializers import ArticleSerializer, ArticleUpdateSerializer



class ArticlesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permission_class = permissions.IsAuthenticatedOrReadOnly

    def create(self, request, *args, **kwargs):

        article = request.data.get('article')
        util = Utils()

        try:
            title = article['title']
            description = article['description']
            body = article['body']
            tags = article['tag_list']
            imageUrl = article['image_url']
            audioUrl = article['image_url']
        except Exception as exception:
            raise APIException({
                'error': f'Required field: {str(exception)} missing!'
            })

        author_id = util.get_token(request)
        if isinstance(author_id, int):
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
                'author': author_id
            }

            serializer = self.serializer_class(data=article)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return author_id


class RetrieveUpdateArticleByIdApiView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        article = Article.objects.get(id=kwargs['pk'])
        article_ = request.data.get('article')

        util = Utils()
        author_id = util.get_token(request)
        if isinstance(author_id, int):
            user = User.objects.get(id=author_id)
            
            if author_id != article.author.id:
                raise APIException({
                    'error': f'Only article author {user.username} can update this article!'
                })
            else:
                new_article = {
                    'slug': article.slug,
                    'title': article_.get('title', article.title),
                    'description': article_.get('description', article.description),
                    'body': article_.get('body', article.body),
                    'tag_list': article_.get('tag_list', article.tag_list),
                    'image_url': article_.get('image_url', article.image_url),
                    'audio_url': article_.get('audio_url', article.audio_url),
                }

                serializer = ArticleUpdateSerializer(data=new_article)
                serializer.is_valid(raise_exception=True)
                serializer.update(article, new_article)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return author_id

    def delete(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=kwargs['pk'])
        except:
            raise APIException({
                'error': f'Article {request.path[14:]} does not exist.'
            })

        util = Utils()
        author_id = util.get_token(request)
        if isinstance(author_id, int):
            user = User.objects.get(id=author_id)
            article_id = article.id

            if author_id != article.author.id:
                raise APIException({
                    'error': f'Only article author {user.username} can update this article!'
                })
            else:
                msg = {'success': f'Article with id: {article_id} deleted!'}
                article.delete()
                return Response(msg, status=status.HTTP_200_OK)
        return author_id



class GetArticleBySlugApiView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permissiion_classes = (permissions.AllowAny, )
    lookup_field = 'slug'

