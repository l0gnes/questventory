from django.shortcuts import get_object_or_404, render, redirect
from .forms import ComprehensiveGameForm, InventorySearchForm, EditGameForm
from .models import Game, Console, GameConsoleStock
from .abstractGameFactory import GameInventoryFactory
from .observerKeepTrackOfStock import global_stock_observer
from django.db.models import Sum
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from .builderPattern import ReceiptDirector, DetailedReceiptBuilder
from django.forms import inlineformset_factory

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
                price = price,
                stock=stock,      
            )    
        return redirect('home.html')
    else:
        form = ComprehensiveGameForm()
    
    notifications = global_stock_observer.get_low_stock_notifications()
    print(notifications) 
    recent_games = Game.objects.annotate(total_stock=Sum('gameconsolestock__stock')).order_by('-id')[:10]
    return render(request, 'home.html', {'form': form, 'recent_games': recent_games, 'low_stock_notifications': notifications})


# This view renders both the inventory list on the inventory page, and also contains
# the relevant functions to integrate the Iterator/Strategy design patterns for
# the searching function.
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


# This is the view that renders all the details for each individual game detail page
# accessed from the inventory page.
# This view also renders the editing function for game entries on the game detail page.
# Unfortunately, this form can't be used to modify the consoles the game is available
# on because the form won't update in real time to add more stock fields.
def gameDetail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    
    # The inlineformset_factory is a Django form function that creates a section of
    # fields on the form that can be used to edit individual game stocks for different consoles.
    StockFormSet = inlineformset_factory(Game, GameConsoleStock, fields=('stock',), extra=0, can_delete=False)
    
    if request.method == 'POST':
        form = EditGameForm(request.POST, instance=game)
        stock_formset = StockFormSet(request.POST, instance=game)
        
        if form.is_valid() and stock_formset.is_valid():
            form.save()
            stock_formset.save()
            messages.success(request, 'Game details updated successfully.')
            return redirect('gameDetail', pk=game.id)
    else:
        form = EditGameForm(instance=game)
        stock_formset = StockFormSet(instance=game)
    
    console_stocks = game.gameconsolestock_set.all()
    return render(request, 'gamedetail.html', {'game': game, 'console_stocks': console_stocks, 'form': form, 'stock_formset': stock_formset})

# Does what it says on the box.
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
    
    # Since the price is recorded in the Game model, we need to access it to get the price.
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
            'price': price_string,
            'stock_id': stock_id
            }
    
    # Saves the cart in the session cookie.
    request.session['cart'] = cart
    
    messages.success(request, 'Item successfully added to cart.')
    
    return redirect('gameDetail', pk=game_id)

# This view is used to render the cart contents on the checkout page with more detail.
# The usage of Decimal is to ensure that the price stored in the session cookie
# is correctly converted from string.
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

# Atomic transaction ensures that all steps of the checkout process are correct.
# If a part of the transaction fails, no transaction happens at all.
@transaction.atomic
def purchase(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('checkout.html')

    # Initialize receipt builder for use in checkout.
    director = ReceiptDirector(DetailedReceiptBuilder())
    
    items = []
    try:
        for key, item in cart.items():
            stock_id = item.get('stock_id')
            quantity = item.get('quantity')
            
            # This code checks to make sure that there's a sufficient amount of stock
            # for the items being purchased. If there's not enough, the purchase will
            # throw an error and not go through.
            print(f"Looking up GameConsoleStock with ID: {stock_id}")  # Debug output
            stock = GameConsoleStock.objects.select_for_update().get(pk=stock_id)
            if stock.stock < quantity:
                raise ValueError(f"Not enough stock for {stock.game.title} on {stock.console.name}.")
            
            stock.stock -= quantity
            stock.save()
        
            # Setting up the dict for the items that'll be placed on the receipt
            # by the builder director.
            dict_items = {
                'title': stock.game.title,
                'console': stock.console.name,
                'quantity': quantity,
                'price': item['price'],
                'subtotal': str(Decimal(item['price']) * quantity)
            }
            items.append(dict_items)
        
        # Using the director defined in the builder pattern to construct the
        # receipt to be displayed.
        director.construct_receipt(items, "Thank you for your purchase!")

        # Clears the session cookie, and the cart goes with it.
        del request.session['cart']
        
    except ValueError as e:
        # Rollback in case of error to make sure the database values don't
        # get messed up.
        transaction.set_rollback(True)
        messages.error(request, str(e))
        return redirect('checkout.html')
    
    receipt = director.get_receipt()
    return render(request, 'receipt.html', {'receipt': receipt})