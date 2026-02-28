from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from .forms import StudentRegistrationForm, StudentLoginForm, ProfileUpdateForm
from .models import User


class RegisterView(View):
    """
    Handles student registration with college email validation.
    """
    template_name = 'accounts/register.html'

    def get(self, request):
        # Redirect already logged-in users
        if request.user.is_authenticated:
            return redirect('marketplace:product_list')
        form = StudentRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email'].lower()
            user.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f"Welcome to Bingo, {user.first_name}! 🎉 Start exploring.")
            return redirect('marketplace:product_list')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """
    Handles student login using email and password.
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('marketplace:product_list')
        form = StudentLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}! 👋")
            # Respect the 'next' parameter for protected redirects
            next_url = request.GET.get('next', 'marketplace:product_list')
            return redirect(next_url)
        messages.error(request, "Invalid email or password. Please try again.")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    Logs out the user and redirects to login page.
    """
    def post(self, request):
        logout(request)
        messages.info(request, "You've been logged out. See you soon!")
        return redirect('accounts:login')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """
    Displays and allows editing of user profile.
    """
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})