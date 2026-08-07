from django.urls import path
from . import views


urlpatterns = [

    path(
        'register/',
        views.register_view,
        name='register'
    ),


    path(
        'login/',
        views.login_view,
        name='login'
    ),


    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),


    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    path(
        'upload/',
        views.upload_resume,
        name='upload_resume'
    ),


    path(
        'resume-history/',
        views.resume_history,
        name='resume_history'
    ),


    path(
    "resume-analysis/<int:resume_id>/",
    views.resume_analysis,
    name="resume_analysis",
    ),

    path(
    "delete-resume/<int:resume_id>/",
    views.delete_resume,
    name="delete_resume"
    ),
]