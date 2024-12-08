from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Author, Title
from .forms import TitleForm

class TitleListView(View):
    def get(self, request):
        titles = Title.objects.all()
        return render(request, 'biblioteka/title_list.html', {'titles': titles})

class TitleDetailView(View):
    def get(self, request, pk):
        title = get_object_or_404(Title, pk=pk)
        return render(request, 'biblioteka/title_detail.html', {'title': title})


class AddTitleView(View):

    def get(self, request):
        form = TitleForm()
        return render(request, 'biblioteka/add_title.html', {'form': form})

    def post(self, request):
        form = TitleForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data.pop('author')
            author, created = Author.objects.get_or_create(name=author_name)
            title = form.save(commit=False)
            title.author = author
            title.save()
            form.save_m2m()
            return redirect('title_list')
        return render(request, 'biblioteka/add_title.html', {'form': form})

class EditTitleView(View):
    def get(self, request, pk):
        book = get_object_or_404(Title, pk=pk)
        form = TitleForm(instance=book)
        return render(request, 'biblioteka/edit_title.html', {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Title, pk=pk)
        form = TitleForm(request.POST, instance=book)
        if form.is_valid():
            title = form.save(commit=False)
            title.author = form.cleaned_data['author']
            title.save()
            form.save_m2m()
            return redirect('title_list')
        return render(request, 'biblioteka/edit_title.html', {'form': form, 'book': book})

class DeleteTitleView(DeleteView):
    model = Title
    template_name = 'biblioteka/delete_title.html'
    success_url = reverse_lazy('title_list')