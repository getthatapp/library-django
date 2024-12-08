from django import forms
from .models import Title, Author, Genre


class TitleForm(forms.ModelForm):
    """
    A form for creating and updating Title instances.

    This form is based on the `Title` model and includes additional customization
    for the `author` and `genre` fields. The form handles author creation dynamically
    and supports multiple genre selection.

    Attributes:
        author (forms.CharField): A text input for entering the author's name.
            It is rendered with a custom ID attribute.
        genre (forms.ModelMultipleChoiceField): A field allowing multiple genre
            selection via checkboxes.
    """
    author = forms.CharField(
        max_length=100,
        label="Author",
        widget=forms.TextInput(attrs={'id': 'id_author'})
    )
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Genre"
    )
    class Meta:
        """
        Meta options for the TitleForm.

        Attributes:
            model (Title): The model associated with this form.
            fields (list): The fields to include in the form.
            widgets (dict): Custom widgets for specific fields.
        """
        model = Title
        fields = ['name', 'description', 'author', 'genre']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the TitleForm.

        Sets the initial value of the `author` field to the name of the associated author
        if the form is bound to an existing instance.
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['author'] = self.instance.author.name

    def clean_author(self):
        """
        Cleans and validates the `author` field.

        Ensures that the provided author name is a string. If the author does not already
        exist in the database, a new `Author` instance is created.

        Returns:
            Author: The existing or newly created Author instance.

        Raises:
            forms.ValidationError: If the provided author name is not a string.
        """
        data = self.cleaned_data['author']
        if not isinstance(data, str):
            raise forms.ValidationError("Must be a text value")
        author, created = Author.objects.get_or_create(name=data)
        return author