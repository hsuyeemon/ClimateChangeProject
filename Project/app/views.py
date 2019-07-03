from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from .models import Book

def get_books(request):
	return render('app/books.html', request, {'books': Book.nodes.all()})