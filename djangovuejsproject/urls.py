"""djangovuejsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from catalog import views
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from catalog import views


v1_router = DefaultRouter()
v1_router.register(r'leads', views.LeadViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^docs/', include_docs_urls(
    title='Bbloom API',
    description='RESTful API (v1)',
#        authentication_classes=[
#            rest_framework_jwt.authentication.JSONWebTokenAuthentication,
#        ],
    permission_classes=(permissions.AllowAny,),
    public=True)),
#    url(r'^leads/$', views.lead_list),
#    url(r'^leads/(?P<pk>[0-9]+)$', views.lead_detail),
    path('admin/', admin.site.urls),
    url(r'^v1/', include(v1_router.urls)),
    url(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html'), name='catchall'),

]

