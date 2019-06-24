from django.urls import path

from . import views

urlpatterns = [
    path('<int:t_uid>', views.transaction, name='transaction'),
    path('self', views.self, name='self'),
    path('flow', views.flow, name='flow'),
]