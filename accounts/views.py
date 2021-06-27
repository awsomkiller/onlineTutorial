from django.shortcuts import redirect, render
from .form import loginForm, studentRegisteration, phonenumber, passwordchange
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from accounts.models import User 
from django import forms

# Create your views here.
def loginview(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = loginForm(request.POST or None)
    if form.is_valid():
        mobile = form.cleaned_data.get("mobileNumber")
        pas = form.cleaned_data.get("password")
        user = authenticate(mobile=mobile, password=pas)
        if user != None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,'login.html',{'form':form, 'invalid_user':True})
    return render(request,'login.html',{'form':form, 'invalid_user':False})

def logoutview(request):
    logout(request)
    return redirect("/")

def registerview(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = studentRegisteration(request.POST or None)
    if form.is_valid():
        mobileNumber = form.cleaned_data.get("mobileNumber")
        password = form.cleaned_data.get("password1")
        fullName = form.cleaned_data.get("fullName")
        emailAddress = form.cleaned_data.get("emailAddress")
        try:
            user = User.objects.create_user(mobileNumber, emailAddress, fullName, password)
        except:
            user = None
        if user !=None:
            login(request, user)
            return redirect("/")
        else :
            request.session['register_error']=1

    return render(request, 'register.html', {'form':form})

def changepassword(request):
    request.session['oldpassword_error']=0
    if request.user.is_authenticated:
        form = passwordchange(request.POST or None)
        if form.is_valid():
            user = User.objects.get(mobile=request.user.mobile)
            oldpassword = form.cleaned_data.get("oldpassword")
            if check_password(oldpassword, request.user.password):
                password1 = form.cleaned_data.get("password1")
                user.set_password(password1)
                return redirect("/")
            else:
                request.session['oldpassword_error']=1
        return render(request, 'changepassword.html', {'form':form})
    else:
        form = phonenumber
        return render(request,'forgetpassword.html',{'form': form})

def otpgeneration(request):
    form = passwordchange
    return render(request, 'changepassword.html', {'form':form})

# class registerview(CreateView):
#     form_class = studentRegisteration
#     template_name = 'register.html'
#     success_url='/login/'

def profileview(request):
    return render(request, 'underconstruction.html')