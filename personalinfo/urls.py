from django.urls import path
from .views import (
    PersonalInfoCreateUpdateView,
    PersonalInfoDeleteView,
)

app_name = 'personalinfo'

urlpatterns = [
    path('resume/<int:resume_id>/personal-info/', PersonalInfoCreateUpdateView.as_view(), name='create_update'),
    path('resume/<int:resume_id>/personal-info/delete/', PersonalInfoDeleteView.as_view(), name='delete'),
]