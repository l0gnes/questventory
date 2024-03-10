from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

def inventory(request):
    return render(request, 'inventory.html')