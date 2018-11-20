from django.urls import path
from .views import (CreateBookMarksView, GetBookMarksView, DeleteBookMarkView)

urlpatterns = [
    path('', GetBookMarksView.as_view(), name='get_bookmark'),
    path('<slug>', CreateBookMarksView.as_view(), name='create_bookmark'),
    path('<slug>/delete', DeleteBookMarkView.as_view(), name='delete_bookmark'),

]
