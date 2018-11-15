from django.urls import path

from .views import (ArticlesListCreateAPIView,
                    GetArticleBySlugApiView, RetrieveUpdateArticleByIdApiView,
                    RateCreateAPIView, RateRetrieveAPIView,
                    )

from .share_articles import (
    ShareArticleViaEmailAPIView,
    ShareArticleViaFacebookAPIView,
    ShareArticleViaTwitterAPIView,
)

from .like_articles import LikeArticlesView

list_create_articles = path(
    '', ArticlesListCreateAPIView.as_view(),  name='list_create_articles')
get_article_byId = path(
    '<int:pk>', RetrieveUpdateArticleByIdApiView.as_view(), name='get_article_byId')
get_article_bySlug = path(
    '<slug:slug>', GetArticleBySlugApiView.as_view(), name='get_article_bySlug')
add_article_ratings = path(
    'add_rates/<slug>', RateCreateAPIView.as_view(), name='add_article_ratings')
view_average_article_ratings = path(
    'view_rates/<slug>', RateRetrieveAPIView.as_view(), name='view_average_article_ratings')
view_article_like_status = path(
    '<int:pk>/like_status', LikeArticlesView.as_view(), name='view_article_like_status')
share_article_via_email = path(
    '<slug>/email', ShareArticleViaEmailAPIView.as_view(), name='share_article_via_email')
share_article_via_facebook = path(
    '<slug>/facebook', ShareArticleViaFacebookAPIView.as_view(), name='share_article_via_facebook')
share_article_via_twitter = path(
    '<slug>/twitter', ShareArticleViaTwitterAPIView.as_view(), name='share_article_via_twitter')

urlpatterns = [
    list_create_articles,
    get_article_byId,
    get_article_bySlug,
    add_article_ratings,
    view_average_article_ratings,
    view_article_like_status,
    share_article_via_email,
    share_article_via_facebook,
    share_article_via_twitter
]
