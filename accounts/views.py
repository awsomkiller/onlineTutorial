from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .form import loginForm, studentRegisteration, phonenumber, passwordchange, otp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from accounts.models import User, otpModel
from django import forms
import random
from datetime import datetime
import urllib.request

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
        form = phonenumber(request.POST or None)
        if form.is_valid():
            n = random.randint(10000, 99999)
            phonenum = form.cleaned_data.get("mobileNumber")
            user = User.objects.filter(mobile=phonenum)
            usersname = user[0].name
            usersname=usersname.split()
            if len(user)<1:
                return redirect("/accounts/register/")
            try:
                otpObj = otpModel.objects.get(phonenumber=phonenum)
                otpObj.otp = n
                otpObj.current_time = datetime.now()
            except otpModel.DoesNotExist:
                otpObj = otpModel(phonenumber=phonenum, otp=n)
            otpObj.save()
            url1 = "http://smsshoot.in/http-tokenkeyapi.php?authentic-key=3739726b656475763934321627812964&senderid=ABHINM&route=2&number="+phonenum+"&message=Dear%20"
            url2 = usersname[0]+"%20OTP%20to%20login%20into%20Rkeduv(account)%20is%"+n+".%20Do%20not%20Share%20with%20anyone.%20-Rkeduv%20abhinm&templateid=1707162694588395444"
            url1 = url1 + url2
            request_url = urllib.request.urlopen(url1)
            request.session['otpid']=phonenum
            return redirect('/accounts/resetpassword/')
        else:
            return render(request,'forgetpassword.html',{'form': form})

def otpgeneration(request):
    form = otp(request.POST or None)
    otpObj = None
    if form.is_valid():
        phonenum = request.session.get('otpid', None)
        if phonenum != None:
            try:
                otpObj = otpModel.objects.get(phonenumber=phonenum)
            except otpModel.DoesNotExist:
                return redirect('/accounts/forgotpassword/')
            timenow = datetime.now()
            time_delta = (timenow - otpObj.current_time)
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            if (minutes > 10):
                try:
                    del request.session['otpid']
                except KeyError:
                        pass
                otpObj.delete()
                return redirect('/accounts/forgotpassword/')
            enteredOtp = form.cleaned_data.get("otp")
            if(enteredOtp == otpObj.otp):
                otpObj.success = True
                otpObj.save()
                return redirect('/accounts/resetpass/')
            else:
                attempt = otpObj.attempt
                attempt +=1
                if attempt<=3:
                    otpObj.attempt = attempt
                    otpObj.save()
                    return render(request, 'otp.html', {'form':form, 'reattempt':True})
                else:
                    try:
                        del request.session['otpid']
                    except KeyError:
                        pass
                    otpObj.delete()
                    return HttpResponse("TO MANY ATTEMPTS")
    else:
        return render(request, 'otp.html', {'form':form, 'reattempt':False})

# class registerview(CreateView):
#     form_class = studentRegisteration
#     template_name = 'register.html'
#     success_url='/login/'

def profileview(request):
    return render(request, 'underconstruction.html')