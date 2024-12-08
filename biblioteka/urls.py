from django.urls import path
from .views import TitleDetailView, TitleListView, AddTitleView, EditTitleView, DeleteTitleView

urlpatterns = [
    path('', TitleListView.as_view(), name='title_list'),
    path('<int:pk>/', TitleDetailView.as_view(), name='title_detail'),
    path('add/', AddTitleView.as_view(), name='add_title'),
    path('<int:pk>/edit/', EditTitleView.as_view(), name='edit_title'),
    path('<int:pk>/delete/', DeleteTitleView.as_view(), name='delete_title'),
]