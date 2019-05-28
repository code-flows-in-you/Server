from django.urls import path

from . import views

urlpatterns = [
    path('', views.publish, name='publish'),
    path('<int:t_aid>', views.controller, name='controller'),
    path('<int:t_aid>/<int:t_qaid>', views.answerHelper, name='answerHelper'),
]