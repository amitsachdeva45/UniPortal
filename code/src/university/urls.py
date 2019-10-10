"""university URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from frontend.views import signup, home, logoutHome#, tempview

urlpatterns = [
    path('admin', admin.site.urls),
    path(r'signup', signup, name='signup'),
    path(r'', home, name='home'),
    #path(r'test1/', tempview, nam(e='temp_view')
    url(r'^logout/', logoutHome, name="logout"),
    url(r'^candidate/', include(('candidate.urls', 'candidate'), namespace="candidate")),
    url(r'^teacher/', include(('teacher.urls', 'teacher'), namespace="teacher"))
]

#Here we are appending static urls with url patterns
# we are using settings.Debug here so that we should keep in mind that on production we should Debug : False
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
