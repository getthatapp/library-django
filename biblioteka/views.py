from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Author, Title
from .forms import TitleForm

class TitleListView(View):
    """
    Handles the display of a list of all titles.

    Methods:
        get(request): Retrieves all Title objects and renders the title list template.
    """
    def get(self, request):
        """
        Retrieves all titles and renders the title list view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered template with the list of titles.
        """
        titles = Title.objects.all()
        return render(request, 'biblioteka/title_list.html', {'titles': titles})

class TitleDetailView(View):
    """
    Handles the display of detailed information about a specific title.

    Methods:
        get(request, pk): Retrieves a single Title object by primary key and renders the detail view.
    """

    def get(self, request, pk):
        """
        Retrieves a specific title and renders the detail view.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the Title to retrieve.

        Returns:
            HttpResponse: The rendered template with the title details.
        """
        title = get_object_or_404(Title, pk=pk)
        return render(request, 'biblioteka/title_detail.html', {'title': title})


class AddTitleView(View):
    """
     Handles the creation of new Title objects.

     Methods:
         get(request): Renders a blank form for creating a new title.
         post(request): Validates and processes the form submission to create a new title.
     """

    def get(self, request):
        """
        Renders a form for creating a new title.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered template with the form.
        """
        form = TitleForm()
        return render(request, 'biblioteka/add_title.html', {'form': form})

    def post(self, request):
        """
        Processes the form submission to create a new title.

        Args:
            request (HttpRequest): The HTTP request object containing form data.

        Returns:
            HttpResponse: A redirect to the title list view on success,
                          or the rendered form with errors on failure.
        """
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
    """
    Handles editing an existing Title object.

    Methods:
        get(request, pk): Retrieves the Title object and renders the edit form.
        post(request, pk): Validates and processes the form submission to update the Title.
    """

    def get(self, request, pk):
        """
        Renders a form for editing an existing title.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the Title to edit.

        Returns:
            HttpResponse: The rendered template with the edit form.
        """
        book = get_object_or_404(Title, pk=pk)
        form = TitleForm(instance=book)
        return render(request, 'biblioteka/edit_title.html', {'form': form, 'book': book})

    def post(self, request, pk):
        """
        Processes the form submission to update the title.

        Args:
            request (HttpRequest): The HTTP request object containing form data.
            pk (int): The primary key of the Title to update.

        Returns:
            HttpResponse: A redirect to the title list view on success,
                          or the rendered form with errors on failure.
        """
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
    """
    Handles deleting a Title object.

    Attributes:
        model (Title): The model associated with this view.
        template_name (str): The template used to confirm deletion.
        success_url (str): The URL to redirect to after successful deletion.
    """
    model = Title
    template_name = 'biblioteka/delete_title.html'
    success_url = reverse_lazy('title_list')