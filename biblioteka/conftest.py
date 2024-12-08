"""
Pytest fixtures for setting up test data in the Library application.

This module contains fixtures that create test data for the `Title`, `Author`, and `Genre` models.
The fixtures are used to set up reusable and consistent test data for unit tests in the Django environment.

Fixtures:
    - `setup_books`: Creates an author, two genres, and two titles with genre associations.
    - `setup_genres`: Creates two genres.

Modules Imported:
    - `pytest`: Provides the fixture decorator and testing utilities.
    - `os` and `django`: Used to configure and initialize the Django environment.
    - Models: `Title`, `Author`, and `Genre` from the application.

Django Setup:
    - The environment variable `DJANGO_SETTINGS_MODULE` is set to point to the `Library.settings` module.
    - `django.setup()` initializes the Django application for standalone script usage.

Fixtures:
    1. `setup_books`:
        - Creates an author: `J.K. Rowling`.
        - Creates two genres: `Fantasy` and `Adventure`.
        - Creates two books:
            - "Harry Plotter" (associated with both genres).
            - "Harry Drukarka" (associated with `Fantasy` only).
        - Returns: A list of the two created `Title` objects.

    2. `setup_genres`:
        - Creates two genres: `Adventure` and `Fantasy`.
        - Returns: A list of the two created `Genre` objects.

Usage:
    Include these fixtures in test cases that require pre-populated `Author`, `Genre`, or `Title` instances.
"""

import pytest
import os
import django
from .models import Title, Author, Genre

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library.settings")
django.setup()

@pytest.fixture
def setup_books(db):
    author = Author.objects.create(name='J.K. Rowling')
    genre_fantasy = Genre.objects.create(name='Fantasy')
    genre_adventure = Genre.objects.create(name='Adventure')
    book1 = Title.objects.create(name="Harry Plotter", author=author)
    book1.genre.add(genre_fantasy, genre_adventure)
    book2 = Title.objects.create(name="Harry Drukarka", author=author)
    book2.genre.add(genre_fantasy)
    return [book1, book2]

@pytest.fixture
def setup_genres(db):
    genre1 = Genre.objects.create(name='Adventure')
    genre2 = Genre.objects.create(name='Fantasy')
    return [genre1, genre2]