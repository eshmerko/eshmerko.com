# urls.py вашего приложения
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('software_updates/', views.software_updates, name='software_updates'),
    path('download/<int:program_id>/', views.download_program, name='download_program'),
]
