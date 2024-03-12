from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from .forms import ComprehensiveGameForm
from .models import Game, Genre, Developer, Console, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory

def home(request):
    # Displays the last 10 added games to the panel on the home page.
    # Also contains the view rendering code for the adding new games modal on the home screen.
    if request.method == 'POST':
        form = ComprehensiveGameForm(request.POST)
        if form.is_valid():
            # Extract data from the form, cleaning it in the process.
            title = form.cleaned_data['title']
            release_date = form.cleaned_data['release_date']
            developer_name = form.cleaned_data['developer']
            genre_ids = [genre.id for genre in form.cleaned_data['genres']]
            console_ids = [console.id for console in form.cleaned_data['consoles']]
            stock = form.cleaned_data['stock']
            
            # Use the factory to create the game and its relationships
            factory = GameInventoryFactory()
            game = factory.create_game(
                title=title,
                release_date=release_date,
                developer_name=developer_name,
                genre_ids=genre_ids,
                console_ids=console_ids,
                stock=stock,
            )
            
            return redirect('home.html')
    else:
        form = ComprehensiveGameForm()
        
    recent_games = Game.objects.all().order_by('-id')[:10]
    return render(request, 'home.html', {'form': form, 'recent_games': recent_games})

def allInventory(request):
    wholeInventory = Game.objects.all().order_by('-id')[0::]
    return render(request, 'inventory.html', {'wholeInventory': wholeInventory})