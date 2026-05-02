from django.urls import path
from .views import course_detail

app_name = 'academy'

urlpatterns = [
    path('course/<int:course_id>/', course_detail, name='course_detail'),
]