from django.urls import path
from . import views

urlpatterns = [
    path('', views.title_list, name='title_list'),
    path('<int:pk>/', views.title_detail, name='title_detail'),
]