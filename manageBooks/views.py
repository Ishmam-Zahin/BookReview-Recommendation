from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Books, UserViewedBooks, Reviews, RecentlyViewedBooks, Ratings
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    context = {}
    return render(request, "manageBooks/home.html", context)

def showDetails(request, id):
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
            book = Books(bookId = id, totalViews = 1)
            viewed = UserViewedBooks(book = book, user = request.user)
            book.save()
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
            isBook = recentBooks.get(bookId = book.bookId)
            isBook.save()
        except:
            if recentBooks.count() >=30:
                tmp = recentBooks[2]
                tmp.bookId = book.bookId
                tmp.save()
            else:
                newRecent = RecentlyViewedBooks(bookId = book.bookId, user = request.user)
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

def getRecentBooks(request, count):
    recentBooks = RecentlyViewedBooks.objects.order_by("-time").values("bookId")
    recentReviewedBooks = Reviews.objects.order_by("-time").values("book_id")
    topViewedBooks = Books.objects.order_by("-totalViews").values("bookId")
    topRatedBooks = Books.objects.order_by("-rating").values("bookId")

    map = {}
    context = {"viewIds": [],
               "reviewIds": [],
               "topViewIds": [],
               "topRateIds": []}
    cc = 0
    for book in recentBooks:
        if cc >= count:
            break
        else:
            try:
                x = map[book["bookId"]]
                continue
            except:
                map[book["bookId"]] = 1
                cc += 1
                context["viewIds"].append(book)
    
    map.clear()
    cc = 0
    for book in recentReviewedBooks:
        if cc >= count:
            break
        else:
            bookId = Books.objects.get(id = book["book_id"]).bookId
            try:
                x = map[bookId]
                continue
            except:
                map[bookId] = 1
                cc += 1
                context["reviewIds"].append({"bookId": bookId})

    map.clear()
    cc = 0
    for book in topViewedBooks:
        if cc >= count:
            break
        else:
            cc += 1
            context["topViewIds"].append(book)
    
    map.clear()
    cc = 0
    for book in topRatedBooks:
        if cc >= count:
            break
        else:
            cc += 1
            context["topRateIds"].append(book)


    # print(topViewedBooks)
    return JsonResponse(context)