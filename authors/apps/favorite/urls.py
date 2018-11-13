
from django.urls import path
from .views import FavoriteArticleView, DeleteFavoriteView

urlpatterns = [
    path('<slug>/favorite', FavoriteArticleView.as_view(), name='favorite_article'),
    path('<slug>/favorite/', DeleteFavoriteView.as_view(), name='delete_favorite')
]
