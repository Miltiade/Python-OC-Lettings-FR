from django.shortcuts import render

def index(request):
    """Render the site homepage."""
    return render(request, 'index.html')
