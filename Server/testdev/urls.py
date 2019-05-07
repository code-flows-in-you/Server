from django.urls import path
from . import views

app_name = 'testdev'
urlpatterns = [
    path('', views.page, name='page'),
]