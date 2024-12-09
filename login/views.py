from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy

# Create your views here.

#Login
class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "registration/login.html"

#Registro
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home") 
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def my_view(request):
    # Esta vista requiere que el usuario esté logeado
    return render(request, 'my_template.html', {'user': request.user})

def another_view(request):
    if request.user.is_authenticated:
        # El usuario está logeado
        return render(request, 'logged_in_template.html', {'user': request.user})
    else:
        # El usuario no está logeado
        return redirect('login')  # Redirect to login page
