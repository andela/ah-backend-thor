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

class GetArticleBySlugApiView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permissiion_classes = (permissions.AllowAny,)
    lookup_field = "slug"



class LikeArticlesView(generics.GenericAPIView):
    serializer_class = ArticleLikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    renderer_class = ArticleLikesRenderer
    lookup_field = 'pk'
    util = Utils()

    def post(self, request, *args, **kwargs):
        article_pk = int(kwargs['pk'])
        if not Article.objects.filter(pk=article_pk).exists():
            raise APIException({
                "error": f"Article with id:{article_pk} does not exist!"
            })

        like_status = request.data.get('like_status')
        author_id = int(self.util.get_token(request))

        if LikeArticle.objects.filter(user=author_id).filter(article=article_pk).exists():
            raise APIException({
                "error": f"You have already liked/disliked Article: {article_pk}!"
            })
        article_data = Article.objects.get(pk=article_pk)
        like_status_new = {
            "article": article_pk,
            "article_title": article_data.title,
            "like_status": like_status,
            "user": author_id
        }

        serializer = self.serializer_class(data=like_status_new)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        article_pk = int(kwargs['pk'])
        if not Article.objects.filter(pk=article_pk).exists():
            raise APIException({
                "error": f"Article with id:{article_pk} does not exist!"
            })
        article_like = LikeArticle.objects.filter(article=article_pk)
        if article_like.exists():
            like_statuses = ArticleLikeSerializer(article_like, many=True)
            return Response(like_statuses.data, status=status.HTTP_200_OK)
        return Response(json.dumps({
            "error": f"Article: {article_pk}, has not been liked/disliked yet!"
        }), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        article_pk = int(kwargs['pk'])
        article = Article.objects.filter(pk=article_pk)
        if not article.exists():
            raise APIException({
                "error": f"Article: {article_pk} not found!"
            })
        author_id = self.util.get_token(request)

        try:
            current_like_status = LikeArticle.objects.get(article=article_pk)

        except:
            raise APIException({
                "error": f"Article : {article_pk} has not been liked/disliked yet!"
            })

        new_like_status = request.data.get(
            'like_status', current_like_status.like_status)
        user_ = User.objects.filter(id=author_id).first()

        if not LikeArticle.objects.filter(user=author_id).filter(article=article_pk).exists():
            raise APIException({
                "error": f"Only {user_.username} can edit this!"
            })
        like_status_updated = {
            "like_status": new_like_status,
        }
        serializer = ArticleLikesUpdateSerializer(data=like_status_updated)
        serializer.is_valid(raise_exception=True)
        serializer.update(current_like_status, like_status_updated)
        return Response(serializer.data, status=status.HTTP_200_OK)
