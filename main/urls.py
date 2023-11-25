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
    path('create-training-samples/', views.create_training_samples, name="create-training-samples"),
    path('reset-training-study/', views.reset_training_study, name="reset-training-study"),
    path('delete-training-samples/', views.delete_training_samples, name="delete-training-samples"),
    path('start-training-study/', views.start_training_study, name="start-training-study"),
    path('training-study/<int:pk>/ ', views.trainining_study, name="training-study"),
    path('user-agreement/', views.process_user_agreement, name="user-agreement"),
    path('user-trust/', views.process_user_trust, name="user-trust"),
    path('jian-scale/', views.process_jian_scale, name="jian-scale"),
]