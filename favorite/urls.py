from django.conf.urls import url, include
from . import views
app_name='favorite'
urlpatterns = [
    url('', views.index,name='index'),
	url('one_day/', views.one_day, name='one_day')
]