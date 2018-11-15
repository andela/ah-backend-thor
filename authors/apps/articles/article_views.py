from .imports import *


class GetArticleBySlugApiView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permissiion_classes = (permissions.AllowAny,)
    lookup_field = "slug"
