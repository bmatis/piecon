from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
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
def settings(request):
    """Show the user their account settings page."""
    return render(request, 'users/settings.html')
