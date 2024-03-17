from django.db import models

class Console(models.Model):
    CONSOLE_CHOICES = [
        ('nintendo switch', 'Nintendo Switch'),
        ('sony playstation 5', 'Sony Playstation 5'),
        ('microsoft xbox series x', 'Microsoft Xbox Series X'),
    ]
    name = models.CharField(max_length=100, choices=CONSOLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Developer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('horror', 'Horror'),
        ('rpg', 'RPG'),
    ]
    name = models.CharField(max_length=50, choices=GENRE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    consoles = models.ManyToManyField(Console, through='GameConsoleStock')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class GameConsoleStock(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    console = models.ForeignKey(Console, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)  # Stock amount, starts at zero.
    is_low_stock = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game', 'console')  # Ensures each game-console pair is unique
    
    # This overwrites the default saving method. It enforces whenever this model is saved
    # to trigger the is_low_stock boolean.    
    def save(self, *args, **kwargs):
        if self.stock < 10:
            self.is_low_stock = True
        else:
            self.is_low_stock = False
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.game.title} on {self.console.get_name_display()} - Stock: {self.stock}"