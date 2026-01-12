from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForms, ProfileUpdateForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie,Booking

def home(request):
    movies = Movie.objects.all()
    return render(request,'home.html',{'movies':movies})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('profile')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # change to your homepage url name
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")

# def login_view(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(request,data=request.POST)
    #     if form.is_valid():
    #         user = form.getuser()
    #         login(request,user)
    #         return redirect('/')
    # else:
    #     form=AuthenticationForm()
    # return render(request,'users/login.html',{'form':form})

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    if request.method == 'POST':
        u_form = UserUpdateForms(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForms(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # ✅ ALWAYS define context outside if/else
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'bookings': bookings
    }

    return render(request, 'users/profile.html', context)


@login_required
def reset_password(request):
    if request.method == 'POST':
        u_form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'u_form':u_form})



 
           
