import json
from rest_framework.renderers import JSONRenderer
from .models import Article
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class ArticlesRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):
        '''
        Returns a dictionary with List of articles
        for 'articles' key and number of articles for
        'articles_count' key
        '''
        if type(data) != ReturnList:
            errors = data.get('error', None)
            if errors != None:
                return super(ArticlesRenderer, self).render(data)
            else:
                return json.dumps({
                    'article': data
                })
        else:
            return json.dumps({
                'articles': data,
                'articles_count': len(Article.objects.all())
            })
