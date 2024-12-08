from django import forms
from .models import Title, Author, Genre


class TitleForm(forms.ModelForm):
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
        model = Title
        fields = ['name', 'description', 'author', 'genre']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['author'] = self.instance.author.name

    def clean_author(self):
        data = self.cleaned_data['author']
        if not isinstance(data, str):
            raise forms.ValidationError("Must be a text value")
        author, created = Author.objects.get_or_create(name=data)
        return author