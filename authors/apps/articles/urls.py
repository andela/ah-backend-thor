from django.urls import path

from .views import (ArticlesListCreateAPIView, LikeArticlesView,
                    GetArticleBySlugApiView, RetrieveUpdateArticleByIdApiView,
                    RateCreateAPIView, RateRetrieveAPIView,)

list_create_articles = path('', ArticlesListCreateAPIView.as_view(),
                            name='list_create_articles')
get_article_byId = path(
    '<int:pk>', RetrieveUpdateArticleByIdApiView.as_view(), name='get_article_byId')
get_article_bySlug = path('<slug:slug>', GetArticleBySlugApiView.as_view(),
                          name='get_article_bySlug')
add_article_ratings = path(
    'add_rates/<slug>', RateCreateAPIView.as_view(), name='add_article_ratings')
view_average_article_ratings = path(
    'view_rates/<slug>', RateRetrieveAPIView.as_view(), name='view_average_article_ratings')
view_article_like_status = path(
    '<int:pk>/like_status', LikeArticlesView.as_view(), name='view_article_like_status')

urlpatterns = [
    list_create_articles,
    get_article_byId,
    get_article_bySlug,
    add_article_ratings,
    view_average_article_ratings,
    view_article_like_status
]
