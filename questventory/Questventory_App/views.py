from django.shortcuts import get_object_or_404, render, redirect
from .forms import ComprehensiveGameForm, InventorySearchForm
from .models import Game, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory
from .observerKeepTrackOfStock import global_stock_observer
from django.db.models import Sum

def home(request):
    
    all_games = Game.objects.all()

    for game in all_games:
    # Retrieve all GameConsoleStock instances for this game
        game_stock_records = GameConsoleStock.objects.filter(game=game)
    
        # Trigger the low stock check for each stock record
        for stock_instance in game_stock_records:
            global_stock_observer.item_sell_callback(stock_instance)
    
    
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
            price = form.cleaned_data['price']
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
            
            #for console_id in [console.id for console in form.cleaned_data['consoles']]:
            #    stock_instance = GameConsoleStock.objects.get(game=game, console_id=console_id)
            #    global_stock_observer.item_sell_callback(stock_instance)    
            
            return redirect('home.html')
    else:
        form = ComprehensiveGameForm()
    
    notifications = global_stock_observer.get_low_stock_notifications()
    print(notifications) 
    recent_games = Game.objects.annotate(total_stock=Sum('gameconsolestock__stock')).order_by('-id')[:10]
    return render(request, 'home.html', {'form': form, 'recent_games': recent_games, 'low_stock_notifications': notifications})

def allInventory(request):
    wholeInventory = Game.objects.annotate(
        total_stock=Sum("gameconsolestock__stock")
    ).order_by("-id")[0::]

    form = InventorySearchForm(request.GET)

    # This should cancel the request from going any further if it's invalid
    if form.is_valid() and len(form.cleaned_data['search_term']) > 0:
    
        search_strategy = InventorySearchForm.get_strategy(
            ctx = wholeInventory,
            strat_str = form.cleaned_data['search_type']
        )

        filtered_results = search_strategy.search(
            s = form.cleaned_data['search_term']
        )

        return render(request, 'inventory.html', {'wholeInventory': filtered_results, 'search_form' : form})
    else:
        return render(request, 'inventory.html', {'wholeInventory': wholeInventory, 'search_form' : form})

def gameDetail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    total_stock = game.gameconsolestock_set.aggregate(Sum('stock'))['stock__sum'] or 0
    return render(request, 'gamedetail.html', {'game': game, 'total_stock': total_stock})

def deleteInventoryEntry(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return redirect('inventory')
