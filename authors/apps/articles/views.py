

from .view_imports import *

from .article_views import (ArticlesFilterSet, ReportArticlesView, LikeArticlesView,
                            GetArticleBySlugApiView)


def article_instance(param):
    query_article = Article.objects.get(slug=param)
    return query_article


class ArticlesFilterSet(FilterSet):
    '''Filters articles based on author_name,title and tags of articles'''
    tags = filters.CharFilter(field_name='tag_list', method='get_tags')
    title = filters.CharFilter()

    def get_tags(self, queryset, name, value):
        return queryset.filter(tag_list__name__contains=value)  # pragma: no cover

    class Meta():
        model = Article
        fields = ['title', 'author__username', 'tags']


class ArticlesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_class = ArticlesRenderer
    permission_class = permissions.IsAuthenticatedOrReadOnly
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticlesFilterSet

    def create(self, request, *args, **kwargs):
        article = request.data.get("article")
        util = Utils()
        try:
            title = article['title']
            description = article['description']
            body = article['body']
            tags = article['tag_list']
            imageUrl = article['image_url']
            audioUrl = article['image_url']
            read_time = (util.article_read_time(
                body, imageUrl) + " minute read")
        except Exception as exception:
            raise APIException(
                {"error": f"Required field: {str(exception)} missing!"})
        author_id = util.get_token(request)
        if isinstance(author_id, int):
            # create unique slug with only alphanumeric characters and dashes for spaces
            slug = ""
            for word in re.split(r"(.)", title.strip().lower()):
                if word.isalnum():
                    slug += word
                elif word.isspace():
                    slug += "_"
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
                'author': author_id,
                'read_time': read_time
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

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=kwargs['pk'])
        article_ = request.data.get('article')
        util = Utils()
        try:
            author_id = util.get_token(request)
        except:
            author_id = 0
        if author_id != article.author.id:
            read_stats = article.read_stats
            read_stats += 1
            new_article = {
                'read_stats': read_stats
            }
            serializer = ArticleUpdateStatsSerializer(
                data=new_article)
            serializer.is_valid(raise_exception=True)
            serializer.update(article, new_article)
        return Response(
            self.serializer_class(
                article, context={'author_id': author_id}).data,
            status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        article = Article.objects.get(id=kwargs["pk"])
        article_ = request.data.get("article")

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
                    'tag_list': article_.get('tag_list', [str(tag) for tag in article.tag_list.all()]),
                    'image_url': article_.get('image_url', article.image_url),
                    'audio_url': article_.get('audio_url', article.audio_url),
                    'read_time': article_.get('read_time', util.article_read_time(article.body, article.image_url))
                }
                serializer = ArticleUpdateSerializer(data=new_article)
                serializer.is_valid(raise_exception=True)
                serializer.update(article, new_article)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return author_id

    def delete(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=kwargs["pk"])
        except:
            raise APIException(
                {"error": f"Article {request.path[14:]} does not exist."}
            )

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


class RateCreateAPIView(generics.CreateAPIView):
    permission_class = permissions.IsAuthenticatedOrReadOnly
    serializer_class = RateSerializer
    look_url_kwarg = "slug"

    def post(self, request, *args, **kwargs):
        """ Add ratings to an article"""
        slug = self.kwargs.get(self.look_url_kwarg)
        self.rate = request.data.get("rate")

        if self.rate > 5:
            return Response(
                {
                    "message": "Rating is only up to 5"
                },
                status=status.HTTP_400_BAD_REQUEST)
        # get id in token:
        token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        decode_token = jwt.decode(
            token, settings.SECRET_KEY, algorithm='HS256')
        user_id = decode_token['id']

        # avoid a question's author from voting
        queried_article = article_instance(slug)
        if queried_article.author.id == user_id and queried_article.slug == slug:
            return Response(
                {
                    "message": "You can not rate your article"
                },
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            data={"rate": self.rate, "user": user_id, 'article': queried_article.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "slug": queried_article.slug, "rating_details": serializer.data
            },
            status=status.HTTP_200_OK)


class RateRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RateSerializer
    look_url_kwarg = "slug"

    def get_queryset(self, *args, **kwargs):
        """ Returns the rating objects for a particular aricle"""
        slug = self.kwargs.get(self.look_url_kwarg)
        queried_article = article_instance(slug)
        queryset = Rate.objects.filter(article=queried_article.id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """ Returns tghe average of an article's ratings"""
        slug = self.kwargs.get(self.look_url_kwarg)
        query = self.get_queryset(self.look_url_kwarg)
        total_count = query.count()

        queried_article = article_instance(slug)
        total_rates = 0
        for rate in query:
            rated = rate.rate
            total_rates += rated
        try:
            av_rating = total_rates / total_count
            return Response(
                {
                    "slug": queried_article.slug, "average_ratings": round(av_rating, 0)
                }, status=status.HTTP_200_OK)
        except:
            return Response(
                {
                    "slug":queried_article.slug,"average_ratings": 0
                    },
                status=status.HTTP_200_OK)
