from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from .forms import ComprehensiveGameForm
from .models import Game, Genre, Developer, Console, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory

# The view for adding games with the abstract factory.
def add_game_with_stock(request):
    if request.method == 'POST':
        form = ComprehensiveGameForm(request.POST)
        if form.is_valid():
            factory = GameInventoryFactory()
            
            # Sets the instance for adding games.
            game = factory.create_game(
                title=form.cleaned_data['title'],
                release_date=form.cleaned_data['release_date'],
                developer=form.cleaned_data['developer'],
            )
            
            game.genres.set(form.cleaned_data['genres'])
            console = form.cleaned_data['console']
            stock = form.cleaned_data['stock']
            factory.manage_game_stock(game_id=game.id, console_id=console.id, stock=stock)
            
            return redirect('add_game.html')
    else:
        form = ComprehensiveGameForm()
    return render(request, 'add_game.html', {'form': form})