from django import forms
from .models import Game, Developer, Console, Genre, GameConsoleStock
from .searchStrategy import (
    SearchStrategyInterface,
    get_strategy
)

class ComprehensiveGameForm(forms.ModelForm):
    # Setting the initial stock for all consoles selected.
    stock = forms.IntegerField(min_value=0, required=True, label="Initial Stock")

    class Meta:
        model = Game
        fields = ['title', 'release_date', 'developer', 'consoles', 'genres', 'price']
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
        self.fields['price'].widget = forms.NumberInput(attrs={'step': '0.01'})

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

class InventorySearchForm(forms.Form):
    # Used on the inventory when searching

    search_term = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search", 
                "class" : 'flex-grow-1 px-2'
            }
        )
    )
    search_type = forms.CharField(
        label="Search by:",
        required=True,
        widget=forms.Select(choices={
            "title" : "Title",
            "console" : "Console",
            "genre" : "Genre",
            "developer" : "Developer",
        }
    ))

    @staticmethod
    def get_strategy(ctx, strat_str : str) -> SearchStrategyInterface:
        return get_strategy(ctx=ctx, type = strat_str)
