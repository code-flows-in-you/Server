from django.urls import path

from . import views

urlpatterns = [
    path('<int:t_pages>', views.getRecentByPages, name='getRecentByPages'),
    path('', views.getRecent, name='getRecent'),
]