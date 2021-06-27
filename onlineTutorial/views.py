from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def commingsoon(request):
    return render(request, 'underconstruction.html')