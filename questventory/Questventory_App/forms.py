from django import forms
from .models import Game, Developer, Console, Genre, GameConsoleStock

class ComprehensiveGameForm(forms.ModelForm):
    # Additional field for stock on a specific console
    stock = forms.IntegerField(min_value=0, required=True, label="Initial Stock")

    class Meta:
        model = Game
        fields = ['title', 'release_date', 'developer', 'consoles', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'consoles': forms.CheckboxSelectMultiple,
            'genres': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initializing the developer, consoles and genres form fields to grab from the DB.
        self.fields['developer'].queryset = Developer.objects.all()
        self.fields['consoles'].queryset = Console.objects.all()
        self.fields['genres'].queryset = Genre.objects.all()

    def save(self, commit=True):
        game = super().save(commit=False)

        # Save the game instance, including many-to-many relationships.
        if commit:
            game.save()
            self.save_m2m()

            # Handling GameConsoleStock model form fields separately.
            for console in self.cleaned_data['consoles']:
                GameConsoleStock.objects.create(
                    game=game,
                    console=console,
                    stock=self.cleaned_data['stock']
                )

        return game