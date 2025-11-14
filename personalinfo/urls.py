from django.urls import path
from .views import (
    PersonalInfoCreateUpdateView,
    PersonalInfoDeleteView,
)

app_name = 'personalinfo'

urlpatterns = [
    # GET - получить, POST - создать, PUT/PATCH - обновить
    path('resume/<int:resume_id>/personal-info/', 
         PersonalInfoCreateUpdateView.as_view(), 
         name='create_update'),
    
    # DELETE - удалить
    path('resume/<int:resume_id>/personal-info/delete/', 
         PersonalInfoDeleteView.as_view(), 
         name='delete'),
]