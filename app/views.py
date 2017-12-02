from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

def main_page(request):
    return HttpResponse("Main Page")

def index(request):
    time_now = timezone.now()
    context = {'time_now': time_now}
    return render(request, 'app/index.html', context)