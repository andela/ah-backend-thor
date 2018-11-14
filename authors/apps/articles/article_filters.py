
from .imports import *

class ArticlesFilterSet(FilterSet):
    '''Filters articles based on author_name,title and tags of articles'''
    tags = filters.CharFilter(field_name='tag_list', method='get_tags')
    title = filters.CharFilter()

    def get_tags(self, queryset, name, value):
        return queryset.filter(tag_list__name__contains=value)

    class Meta():
        model = Article
        fields = ['title', 'author__username', 'tags']
