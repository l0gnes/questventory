from django.db import models

# Database model for consoles
class Console(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Developer(models.Model):
    developerName = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Database model for Genre table
class Genre(models.Model):
    
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('horror', 'Horror')
        ('rpg', 'RPG')
    ]
    
    genreName = models.CharField(max_length=50, choices=GENRE_CHOICES)

    def __str__(self):
        return self.name

# Database model for games, using developers as a foreign key.
class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    consoles = models.ManyToManyField(Console, through = 'GameConsoleStock')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

# Database model to track stock of games per console instead of all combined.    
class GameConsoleStock(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    console = models.ForeignKey(Console, on_delete=models.CASCADE)
    # Stock amount, starts at zero.
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ('game', 'console')  # Ensures each game-console pair is unique

    def __str__(self):
        return f"{self.game.title} on {self.console.name} - Stock: {self.stock}"
