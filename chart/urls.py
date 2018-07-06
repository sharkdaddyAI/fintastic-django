from django.urls import path, include
from . import views
app_name='chart'
urlpatterns = [
    path('', views.index,name='index'),
    path('top20/', views.top20, name='top20'),
    path('us/', views.us, name='us')
]