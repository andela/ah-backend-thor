import json
import re

import time, os

import jwt
from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet,
                                           filters)
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from authors.apps.authentication.models import User
from authors.apps.core.utils.utils import Utils


from .models import Article, LikeArticle, Rate, Report
from .renderers import (ArticleLikesRenderer, ArticleReportsRenderer,
                        ArticlesRenderer)
from .serializers import (ArticleLikeSerializer, ArticleLikesUpdateSerializer,
                          ArticleReportSerializer, ArticleSerializer,
                          ArticleUpdateSerializer, RateSerializer)

