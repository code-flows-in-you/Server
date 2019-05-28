from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('session', views.session, name='session'),
    path('<int:t_uid>', views.getInfo, name='getInfo'),
    path('self', views.self, name='self'),
    path('password', views.changePassword, name='changePassword'),
    path('avatar', views.uploadAvatar, name='uploadAvatar'),
]