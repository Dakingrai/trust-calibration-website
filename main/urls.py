from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-samples/', views.create_study, name="create-samples"),
    path('study/', views.start_study, name="start-study"),
    path('reset-study/', views.reset_study, name="reset-study"),
    path('delete-study/', views.delete_study, name="delete-study"),
    path('generate-report', views.generate_report, name="generate-report"),
    path('study/<int:pk>/ ', views.study, name="study"),
]