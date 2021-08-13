from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import  User, contactus

def home(request):
    return render(request, 'index.html')

def commingsoon(request):
    return render(request, 'underconstruction.html')

def contact(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            issue = request.POST.get('issue', None)
            mess = request.POST.get('message', None)
            us = User.objects.get(mobile=request.user.mobile)
            obj = contactus(reason=1, user=us, message=mess)
            obj.save()
            return HttpResponse('Message submitted')
        else:
            return render(request, 'contactus.html')
    else:
        return redirect('/')