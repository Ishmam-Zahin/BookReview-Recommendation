from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("success")
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
    if request.method == "POST":
        userName = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = userName, password = password)
        if user is not None:
            login(request, user)
            return HttpResponse(f"<h1>success</h1>")
        else:
            messages.success(request, ("error"))
            return redirect("login")
    context = {}
    return render(request, "authentication/login.html", context)