from django.shortcuts import get_object_or_404, render, redirect
from .forms import ComprehensiveGameForm
from .models import Game, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory
from .iteratorSearchByName import GameList
from django.db.models import Sum

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
    
    low_stock_games = GameConsoleStock.objects.filter(is_low_stock=True)    
    recent_games = Game.objects.annotate(total_stock=Sum('gameconsolestock__stock')).order_by('-id')[:10]
    return render(request, 'home.html', {'form': form, 'recent_games': recent_games, 'low_stock_games': low_stock_games})

def allInventory(request):
    wholeInventory = Game.objects.all().order_by('-id')[0::]
    return render(request, 'inventory.html', {'wholeInventory': wholeInventory})

def gameDetail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'gamedetail.html', {'game': game})

def deleteInventoryEntry(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return redirect('inventory')

def search_inventory(request):
    search_query = request.GET.get('search', '')
    all_games = Game.objects.all()
    game_list = GameList(list(all_games))
    if search_query:
        game_list = game_list.search_by_name(search_query)
        
    return render(request, 'inventory_search.html', {'game_list': game_list})