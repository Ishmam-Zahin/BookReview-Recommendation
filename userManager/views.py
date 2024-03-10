from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        return HttpResponse("YOU NEED TO LOG OUT TO REGISTER")
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                context = {}
                return render(request, "authentication/succes.html", context)
            else:
                context = {
                    "form": form,
                }
                return render(request, "authentication/registerForm.html", context) 
    
        form = UserCreationForm
        context = {
            "form": form,
        }
        return render(request, "authentication/registerForm.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        return HttpResponse("YOU ARE ALREADY LOGGED IN!")
    else:
        if request.method == "POST":
            userName = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username = userName, password = password)
            if user is not None:
                login(request, user)
                return redirect(reverse("home"))
            else:
                messages.success(request, ("error"))
                return redirect("login")
        context = {}
        return render(request, "authentication/login.html", context)

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("home"))
    return HttpResponse("you have already logged out!")