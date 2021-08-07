from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .form import loginForm, studentRegisteration, phonenumber, passwordchange, otp, resetpassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from accounts.models import User , otpModel
from datetime import datetime
import random
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
            request.session['otpid']=mobileNumber
            n = random.randint(10000, 99999)
            name = fullName.split()
            try:
                otpObj = otpModel.objects.get(phonenumber=mobileNumber)
                otpObj.otp = n
                otpObj.current_time = datetime.utcnow()
            except otpModel.DoesNotExist:
                otpObj = otpModel(phonenumber=mobileNumber, otp=n, current_time=datetime.utcnow() )
            otpObj.save()
            uphonenum = str(mobileNumber)
            un = str(n)
            url1 = "http://smsshoot.in/http-tokenkeyapi.php?authentic-key=3739726b656475763934321627812964&senderid=ABHINM&route=2&number="+uphonenum+"&message=Dear%20"
            url2 = name[0]+"%20OTP%20to%20login%20into%20Rkeduv(account)%20is%20"+un+".%20Do%20not%20Share%20with%20anyone.%20-Rkeduv%20abhinm&templateid=1707162694588395444"
            url1 = url1 + url2
            request_url = urllib.request.urlopen(url1)
            print(request_url)
            return redirect("/accounts/activate/")
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
                otpObj.current_time = datetime.utcnow()
            except otpModel.DoesNotExist:
                otpObj = otpModel(phonenumber=phonenum, otp=n, current_time=datetime.utcnow() )
            otpObj.save()
            uphonenum = str(phonenum)
            un = str(n)
            url1 = "http://smsshoot.in/http-tokenkeyapi.php?authentic-key=3739726b656475763934321627812964&senderid=ABHINM&route=2&number="+uphonenum+"&message=Dear%20"
            url2 = usersname[0]+"%20OTP%20to%20login%20into%20Rkeduv(account)%20is%20"+un+".%20Do%20not%20Share%20with%20anyone.%20-Rkeduv%20abhinm&templateid=1707162694588395444"
            url1 = url1 + url2
            request_url = urllib.request.urlopen(url1)
            print(request_url)
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
            tz = otpObj.current_time
            tz = tz.replace(tzinfo=None) 
            time_delta = (timenow  - tz)
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/3600
            if (minutes > 10):
                try:
                    del request.session['otpid']
                except KeyError:
                        pass
                otpObj.delete()
                return redirect('/accounts/forgotpassword/')
            enteredOtp = form.cleaned_data.get("otp")
            if(enteredOtp == str(otpObj.otp)):
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

def changepass(request):
    phonenum = request.session.get('otpid', None)
    otpObj =None
    try:
        otpObj = otpModel.objects.get(phonenumber=phonenum)
    except otpModel.DoesNotExist:
            return redirect("/")
    if otpObj.success:            
        form = resetpassword(request.POST or None)
        if form.is_valid():    
            user = User.objects.get(mobile=phonenum)
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if(password1 != password2):
                raise form.ValidationError("Password doesn't match")
            else:
                user.set_password(password1)
                user.save()
                try:
                    del request.session['otpid']
                except KeyError:
                    pass
                otpObj.delete()
                return redirect("/")
        else:
            return render(request, 'resetpass.html',{'form':form})
    return redirect("/")

def profileview(request):
    return render(request, 'underconstruction.html')

def phonenumberactivate(request):
    if request.user.is_authenticated:
        form = otp(request.POST or None)
        otpObj = None
        if form.is_valid():
            phonenum = request.session.get('otpid', None)
            if phonenum != None:
                try:
                    otpObj = otpModel.objects.get(phonenumber=phonenum)
                except otpModel.DoesNotExist:
                    return redirect('/')
                timenow = datetime.now()
                tz = otpObj.current_time
                tz = tz.replace(tzinfo=None) 
                time_delta = (timenow  - tz)
                total_seconds = time_delta.total_seconds()
                minutes = total_seconds/3600
                if (minutes > 10):
                    try:
                        del request.session['otpid']
                    except KeyError:
                            pass
                    otpObj.delete()
                    return redirect('/')
                enteredOtp = form.cleaned_data.get("otp")
                if(enteredOtp == str(otpObj.otp)):
                    user = User.objects.get(mobile=phonenum)
                    user.mobileConfirm = True
                    user.save()
                    try:
                        del request.session['otpid']
                    except KeyError:
                        pass
                    otpObj.delete()
                    return redirect('/')
                else:
                    attempt = otpObj.attempt
                    attempt +=1
                    if attempt<=3:
                        otpObj.attempt = attempt
                        otpObj.save()
                        return render(request, 'activateNumber.html', {'form':form, 'reattempt':True})
                    else:
                        try:
                            del request.session['otpid']
                        except KeyError:
                            pass
                        otpObj.delete()
                        return HttpResponse("TO MANY ATTEMPTS")
        else:
            return render(request, 'activateNumber.html', {'form':form})
    else:
        return redirect('/')

