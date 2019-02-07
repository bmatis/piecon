from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, EmailEditForm


def logout_view(request):
    """Log the user out."""
    logout(request)
    redirect = request.GET.get('next')
    return HttpResponseRedirect(redirect)

def new_account(request):
    """Register a new user."""
    # New account page shouldn't be available to logged in user, so check
    # if already logged in and redirect to main index if they try to access
    # account registration page.
    if request.user.id:
        return HttpResponseRedirect(reverse('main:index'))

    if request.method != 'POST':
        # Display blank registration form.
        form = SignUpForm()
    else:
        # Process completed form.
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('main:index'))

    context = {'form': form}
    return render(request, 'users/new_account.html', context)

@login_required
def change_password(request):
    """Allow a user to change their password."""
    if request.method != 'POST':
        form = PasswordChangeForm(request.user)
    else:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('users:change_password'))

        else:
            messages.error(request, 'Please correct the error(s) below.')

    context = {'form': form}
    return render(request, 'users/change_password.html', context)

@login_required
def settings(request):
    """Show the user their account settings page."""
    return render(request, 'users/settings.html')

@login_required
def edit_email(request):
    """Allow user to change their email address."""
    if request.method != 'POST':
        form = EmailEditForm(instance=request.user)
    else:
        form = EmailEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your email was successfully updated!')
            return HttpResponseRedirect(reverse('users:edit_email'))

        else:
            messages.error(request, 'Please correct the error(s) below.')

    context = {'form': form}
    return render(request, 'users/edit_email.html', context)
