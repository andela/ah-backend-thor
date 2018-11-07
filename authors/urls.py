"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin


from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Author's Haven Api",
        default_version='v1',
        description="A Social platform for the creative at heart",
        terms_of_service="https://ah-backend-thor.herokuapp.com/documentation/",
        contact=openapi.Contact(email="joshua.mugisha@andela.com"),
        license=openapi.License(name="BSD License"),
    ),
    # validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('documentation/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),

    path('api/', include(('authors.apps.authentication.urls',
                          'authors.apps.authentication'), namespace='authentication')),
    path('api/articles/', include(('authors.apps.articles.urls',
                          'authors.apps.articles'), namespace='articles'))
]
