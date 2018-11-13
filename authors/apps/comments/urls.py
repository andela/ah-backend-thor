from django.urls import path
from .views import CommentList, CommentDetail

urlpatterns = [
    path('articles/<slug:slug>/comments/', CommentList.as_view()),
    path('articles/<slug:slug>/comments/<int:pk>', CommentDetail.as_view()),
]
