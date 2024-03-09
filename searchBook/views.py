from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def searchBooks(request):
    context = {}
    return render(request, "searchBook/searchBook.html", context)