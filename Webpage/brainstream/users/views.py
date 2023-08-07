from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.contrib.auth import login
# Create your views here.
def welcome(request):
    if request.user.is_authenticated:
        return redirect(reverse("inicio"))
    else:
        return render(request, "users/bienvenida.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("inicio"))
    else:
        form = CustomUserCreationForm(request.POST)
    return render(request, 'users/register.html', {'form': form})