from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^query/$', views.ticket_query, name = 'query'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
    ]
