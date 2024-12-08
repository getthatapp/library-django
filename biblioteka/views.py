from django.shortcuts import render, get_object_or_404
from models import Title, Author, Genre

def title_list(request):
    titles = Title.objects.all()
    return render(request, 'biblioteka/title_list.html', {'titles': titles})

def title_detail(request, pk):
    title = get_object_or_404(Title, pk=pk)
    return render(request, 'biblioteka/title_detail.html', {'title': title})
