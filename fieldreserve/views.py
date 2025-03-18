from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, You're at the fieldreserve index.")