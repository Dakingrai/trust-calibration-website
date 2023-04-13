from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-samples/', views.create_samples, name="create-samples"),
    path('study/', views.start_study, name="start-study"),
    path('reset-study/', views.reset_study, name="reset-study"),
    path('study/<int:pk>/ ', views.study, name="study"),
]