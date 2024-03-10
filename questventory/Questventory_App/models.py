from django.db import models

# Database model for consoles
class Console(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Developer(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Database model for Genre table
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Database model for games, using developers as a foreign key.
class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    consoles = models.ManyToManyField(Console)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title