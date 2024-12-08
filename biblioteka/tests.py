"""
Test suite for the Library application views.

This module contains pytest functions to test the functionality of views for
the `Title`, `Author`, and `Genre` models. Each test verifies the expected behavior
of the corresponding views under various scenarios.

Fixtures:
    - `client`: Django's test client for simulating requests.
    - `setup_books`: Fixture that sets up test data for books, authors, and genres.
    - `setup_genres`: Fixture that sets up test data for genres.

Tests:
    - `test_title_list_view_get`
    - `test_title_detail_view_get`
    - `test_add_title_view_get`
    - `test_add_title_view_post`
    - `test_edit_title_view_get`
    - `test_edit_title_view_post`
    - `test_delete_title_view`
"""
import pytest
from django.urls import reverse
from .models import Title, Author, Genre

@pytest.mark.django_db
def test_title_list_view_get(client, setup_books):
    """
    Test the GET request for the title list view.

    Ensures that the view returns a 200 status code and that all books
    and their authors are present in the response content.

    Args:
        client: Django's test client.
        setup_books: Fixture that provides test book data.
    """
    url = reverse('title_list')
    response = client.get(url)

    assert response.status_code == 200

    for book in setup_books:
        assert book.name in response.content.decode()
        assert book.author.name in response.content.decode()

@pytest.mark.django_db
def test_title_detail_view_get(client, setup_books):
    """
    Test the GET request for the title detail view.

    Ensures that the view returns a 200 status code and displays
    the book's name, author, and genres in the response content.

    Args:
        client: Django's test client.
        setup_books: Fixture that provides test book data.
    """
    book = setup_books[0]
    url = reverse('title_detail', args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert book.name in response.content.decode()
    assert book.author.name in response.content.decode()
    for genre in book.genre.all():
        assert genre.name in response.content.decode()

@pytest.mark.django_db
def test_add_title_view_get(client, setup_genres):
    """
    Test the GET request for the add title view.

    Ensures that the view returns a 200 status code and displays
    the form fields for creating a new title.

    Args:
        client: Django's test client.
        setup_genres: Fixture that provides test genre data.
    """
    url = reverse('add_title')
    response = client.get(url)

    assert response.status_code == 200
    assert "<form" in response.content.decode()
    assert 'name="name"' in response.content.decode()
    assert 'name="description"' in response.content.decode()
    assert 'name="author"' in response.content.decode()
    assert 'id="id_genre"' in response.content.decode()
    for genre in setup_genres:
        assert genre.name in response.content.decode()

@pytest.mark.django_db
def test_add_title_view_post(client, setup_genres):
    """
    Test the POST request for the add title view.

    Ensures that the view creates a new title, associates it with the
    correct author and genres, and redirects to the title list view.

    Args:
        client: Django's test client.
        setup_genres: Fixture that provides test genre data.
    """
    url = reverse('add_title')
    data= {
        'name': 'Test Book Title',
        'description': 'Test Book Title',
        'author': 'Test Author Name',
        'genre': [genre.id for genre in setup_genres],
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('title_list')
    assert Title.objects.filter(name=data['name']).exists()
    assert Author.objects.filter(name=data['author']).exists()

    book = Title.objects.get(name=data['name'])
    for genre in setup_genres:
        assert genre in book.genre.all()

@pytest.mark.django_db
def test_edit_title_view_get(client, setup_books):
    """
    Test the GET request for the edit title view.

    Ensures that the view returns a 200 status code and pre-fills
    the form with the current data for the specified title.

    Args:
        client: Django's test client.
        setup_books: Fixture that provides test book data.
    """
    book = setup_books[0]
    url = reverse('edit_title', args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "<form" in response.content.decode()
    assert f'value="{book.name}"' in response.content.decode()

@pytest.mark.django_db
def test_edit_title_view_post(client, setup_books, setup_genres):
    """
    Test the POST request for the edit title view.

    Ensures that the view updates the title's name, description, author,
    and genres, and redirects to the title list view.

    Args:
        client: Django's test client.
        setup_books: Fixture that provides test book data.
        setup_genres: Fixture that provides test genre data.
    """
    book = setup_books[0]
    url = reverse('edit_title', args=[book.id])
    data = {
        'name': 'Updated book title',
        'description': 'Updated description',
        'author': 'Updated author',
        'genre': [genre.id for genre in setup_genres],
    }
    response = client.post(url, data)

    assert response.status_code == 302

    book.refresh_from_db()
    assert book.name == 'Updated book title'
    assert book.description == 'Updated description'
    assert book.author.name == 'Updated author'
    for genre in setup_genres:
        assert genre in book.genre.all()

@pytest.mark.django_db
def test_delete_title_view(client, setup_books):
    """
    Test the POST request for the delete title view.

    Ensures that the view deletes the specified title and redirects
    to the title list view.

    Args:
        client: Django's test client.
        setup_books: Fixture that provides test book data.
    """
    book = setup_books[0]
    url = reverse('delete_title', args=[book.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Title.objects.filter(id=book.id).exists()