from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from .models import Profile
from .renderers import ProfileRenderer
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import UpdateView

class UserProfileRetrieveDetailAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        QuerySet = Profile.objects.filter(profile_user__username=self.kwargs["profile_user_id"])
        return QuerySet

    renderer_classes = (ProfileRenderer,)
    serializer_class = UserProfileSerializer


class UserProfileRetrieveAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    renderer_classes = (ProfileRenderer,)
    serializer_class = UserProfileSerializer
