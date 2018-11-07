from django.urls import path

from .views import (ArticlesListCreateAPIView,
                    GetArticleBySlugApiView, RetrieveUpdateArticleByIdApiView)

urlpatterns = [
    path('', ArticlesListCreateAPIView.as_view(),
         name='list_create_articles'),
    path('<int:pk>', RetrieveUpdateArticleByIdApiView.as_view(), name='get_article_byId'),
    path('<slug:slug>', GetArticleBySlugApiView.as_view(),
         name='get_article_bySlug')
]
