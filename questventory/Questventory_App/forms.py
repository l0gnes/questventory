from django import forms
from .models import Game, Console, Developer, Genre, GameConsoleStock

# A form that can handle input to multiple different models (DB Tables) at the same time.
class ComprehensiveGameForm(forms.Form):
    title = forms.CharField(max_length=200)
    release_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    developer = forms.CharField(queryset=Developer.objects.all())
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)
    console = forms.ModelChoiceField(queryset=Console.objects.all())
    stock = forms.IntegerField(min_value=0)