from .models import Article
# from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics
from .serializers import ArticleSerializer
from rest_framework import response
from .filter_serializers import FilterSerializer


class ArticleTagList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """ Return query values using the the tags """
        # tags = self.kwargs['tag_list']
        print(self.kwargs)
        # tags = request.query_params['tag_list']
        # tagged_items = Article.objects.filter(tag_list__contains=tags)
        # print(tagged_items)
        # return tagged_items
        # tag_list = request.query_params['tag_list']

        # tagged_items = Article.objects.filter(
        #     tag_list__contains=tag_list).all()
