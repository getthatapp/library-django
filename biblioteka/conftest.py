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