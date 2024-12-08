"""
URL configuration for the library app.

This module maps URL patterns to corresponding views for the library application.
Each URL pattern is associated with a specific view that handles requests to that URL.

URL Patterns:
    - '' (root): Maps to `TitleListView`, which displays a list of titles.
    - '<int:pk>/': Maps to `TitleDetailView`, which shows details of a specific title by primary key.
    - 'add/': Maps to `AddTitleView`, which provides a form for adding a new title.
    - '<int:pk>/edit/': Maps to `EditTitleView`, which provides a form for editing an existing title.
    - '<int:pk>/delete/': Maps to `DeleteTitleView`, which handles the deletion of a title.

Modules Imported:
    - `path`: Django's utility for routing URLs.
    - Views: TitleDetailView, TitleListView, AddTitleView, EditTitleView, DeleteTitleView from `views.py`.

Usage:
    Include these URL patterns in the project's root URL configuration to integrate
    the library app's functionalities.
"""

from django.urls import path
from .views import TitleDetailView, TitleListView, AddTitleView, EditTitleView, DeleteTitleView

urlpatterns = [
    path('', TitleListView.as_view(), name='title_list'),
    path('<int:pk>/', TitleDetailView.as_view(), name='title_detail'),
    path('add/', AddTitleView.as_view(), name='add_title'),
    path('<int:pk>/edit/', EditTitleView.as_view(), name='edit_title'),
    path('<int:pk>/delete/', DeleteTitleView.as_view(), name='delete_title'),
]