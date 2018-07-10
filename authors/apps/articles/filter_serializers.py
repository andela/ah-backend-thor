from rest_framework import serializers
from .models import Article
from .serializers import ArticleSerializer


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
