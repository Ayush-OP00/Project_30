from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=name
        )

        # 🔥 Manually create Profile
        Profile.objects.create(
            user=user,
            name=name,
            mobile=mobile,
            dob=dob,
            gender=gender,
            address=address
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.name = request.POST.get('name')
        profile.mobile = request.POST.get('mobile')
        profile.dob = request.POST.get('dob')
        profile.gender = request.POST.get('gender')
        profile.address = request.POST.get('address')

        request.user.email = request.POST.get('email')

        profile.save()
        request.user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('dashboard')
    return render(request, 'edit_profile.html', {'profile': profile})
