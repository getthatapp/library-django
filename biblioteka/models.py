from django.db import models

class Author(models.Model):
    """
    Represents an author in the library system.

    This model stores information about authors who can be associated with
    various titles in the library.

    Attributes:
        name (str): The name of the author. Limited to 100 characters.

    Methods:
        __str__(): Returns the name of the author as its string representation.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the Author instance.

        This method is used to represent the Author object by its name,
        making it more readable in the Django admin panel, logs, and other interfaces.

        Returns:
            str: The name of the author.
        """
        return self.name

class Genre(models.Model):
    """
    Represents a genre in the library system.

    This model stores information about different genres that can be
    associated with titles in the library.

    Attributes:
        name (str): The name of the genre. Limited to 50 characters.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        """
        Returns a string representation of the Genre instance.

        This method represents the Genre object by its name,
        making it more user-friendly in the Django admin panel and other interfaces.

        Returns:
            str: The name of the genre.
        """
        return self.name

class Title(models.Model):
    """
    Represents a title in the library system.

    This model stores information about titles, including their name, description,
    associated author, and genres. Titles are linked to a single author and can belong
    to multiple genres.

    Attributes:
        name (str): The name of the title. Limited to 200 characters.
        description (str, optional): A brief description of the title. Can be blank or null.
        author (Author): A foreign key linking the title to a single author. Deleting an author
            will cascade and delete all associated titles.
        genre (Genre): A many-to-many relationship linking the title to multiple genres.

    Methods:
        __str__(): Returns the name of the title as its string representation.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="titles")
    genre = models.ManyToManyField(Genre, related_name="titles")

    def __str__(self):
        """
        Returns a string representation of the Title instance.

        This method represents the Title object by its name,
        making it more user-friendly in the Django admin panel and other interfaces.

        Returns:
            str: The name of the title.
        """
        return self.name
