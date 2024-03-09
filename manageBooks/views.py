from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Books, UserViewedBooks, Reviews
from django.contrib.auth.models import User
# Create your views here.

def showDetails(request, id):
    if request.user.is_authenticated:
        book = {}
        try:
            book = Books.objects.get(bookId = id)
            try:
                viewed = UserViewedBooks.objects.get(book_id = book.id, user_id = request.user.id)
            except:
                viewed = UserViewedBooks(book = book, user = request.user)
                book.totalViews += 1
                viewed.save()
                book.save()
        except:
            book = Books(bookId = id, totalViews = 1)
            viewed = UserViewedBooks(book = book, user = request.user)
            book.save()
            viewed.save()
        canReview = True
        try:
            review = Reviews.objects.get(book = book, user = request.user)
            canReview = False
            print("inlist")
        except:
            canReview = True
            print("not in list")
        context = {
            "book": book,
            "canReview": canReview,
        }
        return render(request, "manageBooks/bookDetail.html", context)

    return HttpResponse("you must log in to do that!")

def getReviews(request, id):
    if request.user.is_authenticated:
        book = Books.objects.get(bookId = id)
        reviews = book.reviews_set.all()
        context = {"reviews": []}
        for review in reviews:
            tmp = {}
            tmp["message"] = review.message
            tmp["userName"] = review.user.username
            context["reviews"].append(tmp)
        return JsonResponse(context)
    return JsonResponse({})

def postReview(request, id):
    if request.user.is_authenticated:
        book = Books.objects.get(bookId = id)
        user = request.user
        msg = request.POST["message"]
        review = Reviews(message = msg, user = user, book = book)
        review.save()
    return redirect(reverse("details", args=(id,)))