# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.
from finance.models import payment, checkoutrecord
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
import stripe
from accounts.models import User, subscriptionplan
import environ
import os
import datetime

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

if settings.DEBUG:
    success=env('TEST_SUCCESS')
    cancel=env('TEST_CANCEL')
    stripe.api_key = env('STRIPE_TEST_KEY')
else:
    stripe.api_key = env('STRIPE_LIVE_KEY')
    success=env('SUCCESS')
    cancel=env('CANCEL')

def create_checkout_session(request):
    #CHECK USER AUTHENTICATION
    if request.user.is_authenticated:
        #CHECK SESSION TIME
        checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
        checkoutobj = checkoutobj[0]
        timeNow = datetime.datetime.now()
        timedifference =  timeNow - checkoutobj.time
        duration = timedifference.total_seconds()
        duration = duration / 60
        #IF DURATION IS LESS 10 MINS
        if duration>10:
            amount =  checkoutobj.amount
            amount = amount*100
            title = checkoutobj.plan
            title = title.title
            #STRIPE REQUEST MUST BE POST
            if request.method == 'POST':
                session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': title,
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
                }],
                mode='payment',
                success_url=success,
                cancel_url=cancel,
                )
                return redirect(session.url, code=303)
            else:
                return HttpResponse("INVALID REQUEST")
        else:
            return HttpResponse("Session time is out, please try again.")
    else:
        request.session['redirect'] = 11
        return redirect('/accounts/login/')

def success_url(request):
    user=User.objects.get(mobile=request.user.mobile)
    user.fees = True
    user.save()
    obj = payment(user=user)
    obj.save()
    return HttpResponse('Success')

def cancel_url(request):
    return HttpResponse('Cancel')

def checkout(request):
    return render(request, 'checkout.html')

#DISPLAYS AVAILABLE ACTIVE PLANS
def userplans(request):
    return render(request, 'userplans.html')

def selectplans(request, planid=-1):
    #CHECK USER IS AUTHENTICATED
    if request.user.is_authenticated():
        #GET CURRENT TIME
        timenow = datetime.datetime.now()
        if planid == -1:
            #NO PLAN ID PASSED, REDIRECTING TO AVAILABLE PLAN OPTIONS.
            return redirect('/finance/user-plan/')
        else:
            current_plan = request.user.plan
            new_plan = subscriptionplan.objects.get(id=planid)

            #CHECKING FOR AN REATTEMPT
            if checkoutrecord.objects.filter(user=request.user, isactive=True).exists():
                existingcheckout = checkoutrecord.objects.get(user=request.user)
                existingcheckout.plan = new_plan
                existingcheckout.time = timenow
                existingcheckout.status = "attempting"
                existingcheckout.save()
            else:
                #IF STUDENT HAVE NO ACTIVE PLAN
                if current_plan is None:
                    if request.user.institute:
                        #INSTITUTE STUDENT
                        planprice = int(new_plan.discounted_price)
                    else:
                        #OUTSIDER
                        planprice = int(new_plan.normal_cost)
                    checkOutObject = checkoutrecord(user=request.user, plan=new_plan, amount=planprice, time=timenow, status="attempting")
                    checkOutObject.save()
                #STUDENT HAVE PRE-EXISTING PLAN
                else:
                    if request.user.institute:
                        #INSTITUTE STUDENT
                        planprice = (new_plan.discounted_price)-int(current_plan.discounted_price)
                    else:
                        #OUTSIDER
                        planprice = int(new_plan.normal_cost)-int(current_plan.discounted_price)

                    #CHECK NEW PLAN IS GREATER THEN ACTIVE PLAN
                    if planprice < 0:
                        HttpResponse('Invalid Response')
                    else:
                        #ADDING PLAN CHANGE CHARGERS OF 100
                        planprice = planprice + 100
                    checkOutObject = checkoutrecord(user=request.user, plan=new_plan, amount=planprice, time=timenow, status="attempting")
                    checkOutObject.save()
            return redirect('/finance/checkout/')
    else:
        request.session['redirect'] = 11
        return redirect('/accounts/login/')
            
            