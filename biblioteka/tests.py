import pytest
from django.urls import reverse
from .models import Title, Author, Genre

@pytest.mark.django_db
def test_title_list_view_get(client, setup_books):
    url = reverse('title_list')
    response = client.get(url)

    assert response.status_code == 200

    for book in setup_books:
        assert book.name in response.content.decode()
        assert book.author.name in response.content.decode()

@pytest.mark.django_db
def test_title_detail_view_get(client, setup_books):
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
    book = setup_books[0]
    url = reverse('edit_title', args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "<form" in response.content.decode()
    assert f'value="{book.name}"' in response.content.decode()

@pytest.mark.django_db
def test_edit_title_view_post(client, setup_books, setup_genres):
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
    book = setup_books[0]
    url = reverse('delete_title', args=[book.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Title.objects.filter(id=book.id).exists()