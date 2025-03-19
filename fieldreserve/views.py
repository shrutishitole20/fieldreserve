from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user_name = request.user.username
    context = {
        'username': user_name,
    }
    return render(request, 'index.html', context)

# Define the index view to use the same logic as home
index = home