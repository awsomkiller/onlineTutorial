from django import forms
from django.http import request
from accounts.models import User
import re
from django.contrib import messages

class studentRegisteration(forms.Form):
    class Meta:
        model = User
    fullName = forms.CharField(label='', max_length=100)
    emailAddress = forms.EmailField(label='')
    mobileNumber = forms.CharField(label='', max_length=10,min_length=10)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(),min_length=6)

    fullName.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Your Full Name'
    })
    emailAddress.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Email Address'
    })
    mobileNumber.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Mobile Number'
    })
    password1.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Password'
    })
    password2.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Re-Enter Password'
    })
    def clean_fullName(self):
        fullName = self.cleaned_data.get("fullName")
        return fullName

    def clean_mobileNumber(self):
        mobile = self.cleaned_data.get("mobileNumber")
        pattern = re.compile(r'[0-9]{10}', re.IGNORECASE)
        matches = pattern.match(mobile)
        if (matches):
            qs  = User.objects.filter(mobile=mobile)
            if qs.exists():
                raise forms.ValidationError("This phone number is already in use.")
            return mobile
        else:
            # raise forms.ValidationError("Invalid Phone Number")
            messages.info(request, 'Invalid Mobile number')
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        return password2

    def clean_emailAddress(self):
        emailAddress = self.cleaned_data.get("emailAddress")
        emailAddress = emailAddress.lower()
        qs = User.objects.filter(email=emailAddress)
        if qs.exists():
            raise forms.ValidationError("This emailAddress is already in use")
        return emailAddress
    
    def save(self, commit=True):
        user = super(studentRegisteration, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class loginForm(forms.Form):
    mobileNumber = forms.CharField(label='', max_length=10)
    password = forms.CharField(label='', widget=forms.PasswordInput())

    mobileNumber.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Mobile Number'
    })
    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Password'
    })

    def clean_mobileNumber(self):
        mobileNumber = self.cleaned_data.get("mobileNumber")
        pattern = re.compile(r'[0-9]{10}', re.IGNORECASE)
        matches = pattern.match(mobileNumber)
        if(matches):
            qs  = User.objects.filter(mobile=mobileNumber)
            if not qs.exists():
                raise forms.ValidationError("This is invalid user.")
            return mobileNumber
        else:
            raise forms.ValidationError("Invalid Mobile number")

    # def clean(self):
    #     mobileNumber = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

class phonenumber(forms.Form):
    mobileNumber = forms.CharField(label='', max_length=10)

    mobileNumber.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter mobile number'
    })
    # def clean_mobileNumber(self):
    #     mobileNumber = self.cleaned_data.get("mobileNumber")
    #     pattern = re.compile(r'[0-9]{10}', re.IGNORECASE)
    #     matches = pattern.match(mobileNumber)
    #     if(matches):
    #         return mobileNumber

class otp(forms.Form):
    otp = forms.CharField(label='', max_length=5)

    otp.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter OTP'
    })

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        return otp

class passwordchange(forms.Form):
    oldpassword = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)

    oldpassword.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Old Password'
    })
    password1.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Password'
    })
    password2.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Re-Enter Password'
    })

    def clean_oldpassword(self):
        oldpassword =  self.cleaned_data.get("oldpassword")
        return oldpassword

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if(password1 != password2):
            raise forms.ValidationError("Password doesn't match")
        return password2

class resetpassword(forms.Form):
    password1 = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(), min_length=6)
    password1.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Enter Password'
    })
    password2.widget.attrs.update({
        'class': 'form-control',
        'placeholder':'Re-Enter Password'
    })
