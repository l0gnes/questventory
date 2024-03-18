from django.shortcuts import get_object_or_404, render, redirect
from .forms import ComprehensiveGameForm, InventorySearchForm
from .models import Game, Console, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory
from .observerKeepTrackOfStock import global_stock_observer
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal

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
    console_stocks = game.gameconsolestock_set.all()
    return render(request, 'gamedetail.html', {'game': game, 'console_stocks': console_stocks})

def deleteInventoryEntry(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return redirect('inventory')

@require_POST
def addToCart(request, stock_id):
    game_id = request.POST.get('game_id')
    console_id = request.POST.get('console_id')
    
    # Using Django sessions to store cart inventory as a cookie that can be accessed
    # by the builder design pattern to create a receipt during the checkout page.
    cart = request.session.get('cart', {})
    
    # Creates a unique pair for the game-console combination in the cart.
    cart_pair = f"{game_id}_{console_id}"
    
    # Fetch the game to get the price associated with it.
    game = get_object_or_404(Game, pk=game_id)
    
    # Since Django uses JSON for sessions, the price needs to be converted to a string
    # otherwise you get a "Object of type Decimal is not JSON serializable" error.
    price_string = str(game.price) 
    
    # If the game-console pair is already in the cart, then the amount increments by 1.
    # If the game-console pair isn't already in the cart, it creates a new pair to add.
    if cart_pair in cart:
        cart[cart_pair]['quantity'] += 1
    else:
        cart[cart_pair] = {
            'game_id': game_id, 
            'console_id': console_id, 
            'quantity': 1,
            'price': price_string
            }
    
    # Saves the cart in the session cookie.
    request.session['cart'] = cart
    
    messages.success(request, 'Item successfully added to cart.')
    
    return redirect('gameDetail', pk=game_id)

def displayCart(request):
    cart = request.session.get('cart', {})
    detailed_cart = []
    total_cost = Decimal('0.00')
    
    for key, item in cart.items():
        game = Game.objects.get(pk=item['game_id'])
        console = Console.objects.get(pk=item['console_id'])
        price = Decimal(item['price'])
        item_total = item['quantity'] * price
        total_cost += item_total
        detailed_cart.append({
            'game_title': game.title,
            'console': console.name,
            'quantity': item['quantity'],
            'price': game.price,
            'item_total': item_total,
        })
    
    return render(request, 'checkout.html', {'cart': detailed_cart, 'total_cost': total_cost})