from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

def index(request):
    return HttpResponse("<h2>Hello Deep learning server!</h2>")

def get_file_url(request):
    return HttpResponse('Hello From get_file_url')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

