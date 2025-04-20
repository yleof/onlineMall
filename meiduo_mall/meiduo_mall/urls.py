"""
URL configuration for meiduo_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from django.http import HttpResponse

from utils.converters import *
from django.urls import register_converter

register_converter(UsernameConverter,'username')
register_converter(MobileConverter, 'mobile')
register_converter(UUIDConverter, 'uuid')


# def log(request):

#     import logging
#     logger = logging.getLogger('django')
#     logger.info('login')
#     logger.warning('redis out of memory')
#     logger.error('error')
#     logger.debug('~~~~~')

#     return HttpResponse('log')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('log/', log),
    path('', include('apps.users.urls')),
    path('', include('apps.verifications.urls')),
]
