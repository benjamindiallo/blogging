"""blogging URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blogging.profiles import views

urlpatterns = [
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w.@+-]+)/followers$', views.followers, name='followers'),
    url(r'^profile/(?P<username>[\w.@+-]+)/followings$', views.followings, name='followings'),
    url(r'^follow/', views.follow, name='follow'),
    url(r'^unfollow/', views.unfollow, name='unfollow'),
    url(r'^users/$', views.UserListView.as_view(), name='users'),
]
