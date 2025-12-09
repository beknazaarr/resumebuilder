# backend/personalinfo/urls.py
from django.urls import path
from .views import (
    PersonalInfoCreateUpdateView,
    PersonalInfoDeleteView,
)

app_name = 'personalinfo'

urlpatterns = [
    # Изменено с 'resume' на 'resumes' для согласованности
    path('resumes/<int:resume_id>/personal-info/', 
         PersonalInfoCreateUpdateView.as_view(), 
         name='create_update'),
    
    path('resumes/<int:resume_id>/personal-info/delete/', 
         PersonalInfoDeleteView.as_view(), 
         name='delete'),
]