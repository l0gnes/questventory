"""
URL configuration for questventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from Questventory_App import views


# Django uses URL path configurations to determine which views should be rendered
# and also defines the URL that you see. Some of the URLs, like the gamedetail and
# addToCart use the primary key (pk) for functions.

urlpatterns = [
    path('', RedirectView.as_view(url='/home.html')),
    path('admin/', admin.site.urls),
    path('home.html', views.home, name='home'),
    path('inventory.html', views.allInventory, name='inventory'),
    path('inventory.html', views.allInventory, name='search_inventory'),
    path('gamedetail/<int:pk>', views.gameDetail, name='gameDetail' ),
    path('gamedetail/<int:pk>', views.gameDetail, name='editGame' ),
    path('gamedetail/delete/<int:pk>/', views.deleteInventoryEntry, name='deleteInventoryEntry'),
    path('addToCart/<int:stock_id>/', views.addToCart, name='addToCart'),
    path('checkout.html', views.displayCart, name='checkout'),
    path('receipt.html', views.purchase, name='purchase')
]

