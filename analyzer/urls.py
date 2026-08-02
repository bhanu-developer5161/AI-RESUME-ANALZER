from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name="upload_resume"),
    path('dashboard/<int:resume_id>/', views.dashboard, name="dashboard"),
]