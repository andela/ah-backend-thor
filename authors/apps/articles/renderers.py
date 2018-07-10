import json
from rest_framework.renderers import JSONRenderer

from .models import Article, LikeArticle, Report

from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class BaseRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type= None, render_context=None):

        '''
        Returns a dictionary with List of articles
        for 'articles' key and number of articles for
        'articles_count' key
        '''
        if type(data) != ReturnList:
            errors = data.get('error', None)
            if errors != None:
                return super(BaseRenderer, self).render(data)
            else:
                return json.dumps({
                    self.name: data
                })
        else:
            return json.dumps({
                self.name: data,
                self.name: len(self.model.objects.all()) 

            })

base = BaseRenderer()

class ArticlesRenderer:
    charset = 'utf-8'
    base.name = 'articles'
    base.model = Article

class ArticleLikesRenderer:
    charset = 'utf-8'
    base.name = 'like_status'
    base.model = LikeArticle

class ArticleReportsRenderer:
    charset = 'utf-8'
    base.name = 'reported'
    base.model = Report

