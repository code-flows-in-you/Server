from django.urls import path

from . import views

urlpatterns = [
    path('<int:t_pages>', views.getRecentByPages, name='getRecentByPages'),
    path('', views.getRecent, name='getRecent'),
    path('<str:t_class>', views.getRecentByClass, name='getRecentByClass'),
    path('<str:t_class>/<int:t_pages>', views.getRecentByClassAndPages, name='getRecentByClassAndPages'),
]