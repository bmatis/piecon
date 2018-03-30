from django.shortcuts import render

def index(request):
    """The home page for the PieCon site."""
    return render(request, 'main/index.html')
