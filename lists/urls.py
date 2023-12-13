from django.conf.urls import url
from django.urls import path
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
]
