from django.urls import path
from .views import CommentList, CommentDetail, CommentLike, CommentDislike

urlpatterns = [
    path('articles/<slug:slug>/comments/', CommentList.as_view()),
    path('articles/<slug:slug>/comments/<int:pk>', CommentDetail.as_view()),
    path('<int:pk>/like',
         CommentLike.as_view()),
    path('<int:pk>/dislike',
         CommentDislike.as_view())

]
