from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Books, UserViewedBooks, Reviews, RecentlyViewedBooks, Ratings
from django.contrib.auth.models import User
import requests
# Create your views here.

def insertBook(bookId):
    book = Books(bookId = bookId, totalViews = 1)
    book.save()
    endpoint = ('https://www.googleapis.com/books/v1/volumes/'+ bookId)
    get_response = requests.get(endpoint)
    data = get_response.json()
    # print(data)
    try:
        book.author = data['volumeInfo']['authors'][0]
    except:
        book.author = 'undefined'
    
    try:
        book.publisher = data['volumeInfo']['publisher']
    except:
        book.publisher = 'undefined'
    
    try:
        book.publishDate = data['volumeInfo']['publishedDate']
    except:
        book.publishDate = 'undefined'
    
    try:
        book.title = data['volumeInfo']['title']
    except:
        book.title = 'undefined'

    try:
        tmp = data['volumeInfo']['imageLinks']
        try:
            book.imageLink = data['volumeInfo']['imageLinks']['thumbnail']
        except:
            try:
                book.imageLink = data['volumeInfo']['imageLinks']['smallThumbnail']
            except:
                book.imageLink = '/static/manageBooks/resources/brokenImage.jpg'
    except:
        book.imageLink = '/static/manageBooks/resources/brokenImage.jpg'

    try:
        book.description = data['volumeInfo']['description']
    except:
        book.description = 'undefined'

    book.save()
    return book


def home(request):
    context = {}
    return render(request, "manageBooks/home.html", context)

def showDetails(request, id):
    # insertBook(id)
    if request.user.is_authenticated:
        book = {}
        #check if the book is already in database or not
        try:
            book = Books.objects.get(bookId = id)
            #check if the user is already viewed the book or not
            try:
                viewed = UserViewedBooks.objects.get(book_id = book.id, user_id = request.user.id)
            except:
                viewed = UserViewedBooks(book = book, user = request.user)
                book.totalViews += 1
                viewed.save()
                book.save()
        except:
            book = insertBook(id)
            # book = Books.objects.get(bookId = id)
            viewed = UserViewedBooks(book = book, user = request.user)
            viewed.save()

        #check if the user is able to post reviews
        canReview = True
        try:
            review = Reviews.objects.get(book = book, user = request.user)
            canReview = False
        except:
            canReview = True
        
        #check if the user is able to post rateing
        canRate = True
        try:
            rate = Ratings.objects.get(book = book, user = request.user)
            canRate = False
        except:
            canRate = True

        context = {
            "book": book,
            "canReview": canReview,
            "canRate": canRate,
        }

        #update the book as user's recently viewed book
        recentBooks = RecentlyViewedBooks.objects.filter(user = request.user).order_by("-time")
        try:
            isBook = recentBooks.get(book = book)
            isBook.save()
        except:
            if recentBooks.count() >=30:
                tmp = recentBooks[29]
                tmp.book = book
                tmp.save()
            else:
                newRecent = RecentlyViewedBooks(book = book, user = request.user)
                newRecent.save()

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
        if msg != "":
            review = Reviews(message = msg, user = user, book = book)
            review.save()
    return redirect(reverse("details", args=(id,)))

def postRating(request, id):
    if request.user.is_authenticated:
        book = Books.objects.get(bookId = id)
        user = request.user
        try:
            rating = Ratings.objects.get(user = user, book = book)
        except:
            rate = int(request.POST["rating"])
            newRating = Ratings(rate = rate, user = user, book = book)
            newRating.save()
            previousAvgRating = book.rating * book.totalRatingCount
            newTotalRatingCount = book.totalRatingCount + 1
            newAvgRating = round(((previousAvgRating + rate) / newTotalRatingCount), 2)
            book.rating = newAvgRating
            book.totalRatingCount = newTotalRatingCount
            book.save()

    return redirect(reverse("details", args=(id,)))

def serializeBook(book):
    context = {
        'bookId': book.bookId,
        'totalViews': book.totalViews,
        'rating': book.rating,
        'author': book.author,
        'publisher': book.publisher,
        'publishDate': book.publishDate,
        'title': book.title,
        'description': book.description,
        'imageLink': book.imageLink,
    }

    return context


def getRecentBooks(request, count):
    recentBooks = RecentlyViewedBooks.objects.order_by("-time")
    recentReviewedBooks = Reviews.objects.order_by("-time")
    topViewedBooks = Books.objects.order_by("-totalViews")
    topRatedBooks = Books.objects.order_by("-rating")

    map = {}
    context = {"viewBooks": [],
               "reviewBooks": [],
               "topViewBooks": [],
               "topRateBooks": [],
               }
    cc = 0
    for book in recentBooks:
        if cc >= count:
            break
        else:
            try:
                x = map[book.book.bookId]
                continue
            except:
                map[book.book.bookId] = 1
                cc += 1
                context["viewBooks"].append(serializeBook(book.book))
    
    map.clear()
    cc = 0
    for book in recentReviewedBooks:
        if cc >= count:
            break
        else:
            try:
                x = map[book.book.bookId]
                continue
            except:
                map[book.book.bookId] = 1
                cc += 1
                context["reviewBooks"].append(serializeBook(book.book))

    map.clear()
    cc = 0
    for book in topViewedBooks:
        if cc >= count:
            break
        else:
            cc += 1
            context["topViewBooks"].append(serializeBook(book))
    
    map.clear()
    cc = 0
    for book in topRatedBooks:
        if cc >= count:
            break
        else:
            cc += 1
            context["topRateBooks"].append(serializeBook(book))

    return JsonResponse(context)