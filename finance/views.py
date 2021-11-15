# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.
from finance.models import payment, checkoutrecord, trynowrecord
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
from accounts.models import User, subscriptionplan
import environ
import os
import datetime
import pytz

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
    endpoint_secret = env('ENDPOINT_SECRET')

def create_checkout_session(request):
    #CHECK USER AUTHENTICATION
    if request.user.is_authenticated:
        #CHECK SESSION TIME
        checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
        checkoutobj = checkoutobj[0]
        timeNow = datetime.datetime.now(pytz.utc)
        dt = checkoutobj.time
        dt.replace(tzinfo=None)
        timedifference =  timeNow - dt
        duration = timedifference.total_seconds()
        duration = duration / 60
        #IF DURATION IS LESS 10 MINS
        if duration<10:
            amount =  int(checkoutobj.amount)
            amount = amount*100
            plan = checkoutobj.plan
            title = plan.title
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
        request.session['redirectUrl'] = "/finance/create-checkout-session/"
        return redirect('/accounts/login/')

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event Change it for prof appeal
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
        checkoutobj.isactive=False 
        checkoutobj.save()
        paymentRecord = payment(user = request.user, plan = checkoutobj.plan, amount=checkoutobj.amount)
        paymentRecord.save()
        user = User.objects.get(mobile = request.user.mobile)
        user.plan = checkoutobj.plan
        user.save()

    # Passed signature verification
    return HttpResponse(status=200)

def success_url(request):
    checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
    checkoutobj = checkoutobj[0]
    checkoutobj.status = "success"
    checkoutobj.save()
    return HttpResponse('Success')

def cancel_url(request):
    checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
    checkoutobj = checkoutobj[0]
    checkoutobj.status = "cancel"
    checkoutobj.isActive = False
    checkoutobj.save()
    return redirect('/finance/user-plan/')

def checkout(request):
    return render(request, 'checkout.html')

#DISPLAYS AVAILABLE ACTIVE PLANS
def userplans(request):
    #CHECK USER IS AUTHENTICATED
    if request.user.is_authenticated:
        #CHECK USER IS SUBSCRIBED TO AN PLAN
        currentPlan = request.user.plan
        if request.user.plan is not None:
            allPlans = subscriptionplan.objects.filter(active=True)
            currentPlanPrice = currentPlan.normal_cost
            planset = []
            for plan in allPlans:
                if plan.normal_cost > currentPlanPrice:
                    #ADDING PLAN CHANGE CHARGES
                    plan.normal_cost = str(int(plan.normal_cost) + 100)
                    plan.discounted_price = str(int(plan.discounted_price) + 100)
                    planset.append(plan)
            #IF THERE IS NO HIGHER PLANS AVAILABLE
            if len(planset) == 0:
                return HttpResponse("You're already on the highest plan")
            return render(request, 'userplans.html', {'allPlans':planset})
        else:
            #PASSING ALL THE PLANS
            allPlans = subscriptionplan.objects.filter(active=True)
            tryPlatform = True
            return render(request, 'userplans.html', {'allPlans':allPlans, 'currentPlan':currentPlan, 'tryPlatform':tryPlatform})
    else:
        #Set redirect code
        request.session['redirectUrl'] = "/finance/user-plan/"
        return redirect('/accounts/login/')


#PLAN SELECTION AND ALLOCATION
def selectplans(request, planid=-1):
    #CHECK USER IS AUTHENTICATED
    if request.user.is_authenticated:
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
                        planprice = int(new_plan.discounted_price)-int(current_plan.discounted_price)
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
        request.session['redirectUrl'] = "/finance/user-plan/select-plan=" + str(planid) + "/"
        return redirect('/accounts/login/')
           
def try_now(request):
    #CHECK USER IS AUTHENTICATED
    if request.user.is_authenticated:
        #CHECK USER HAS ALREADY ACTIVATED TO FREE TRIAL.
        if trynowrecord.objects.filter(user=request.user, active=True).exists():
            tryNow = trynowrecord.objects.filter(user=request.user, active=True)
            timeNow = datetime.datetime.now(pytz.utc)
            #CHECK TRIAL EXPIRY.
            if(timeNow>tryNow.endtime):
                tryNow.active = False
                tryNow.save()
            #REDIRECT TO OPT A NEW PLAN
            return redirect('/finance/user-plans/')
        else:
            #ACTIVATE TRIAL PERIOD
            #APPLY PLAN FOR THE USER
            user = User.objects.get(mobile = request.user.mobile)
            #GET FREE TRIAL PLAN
            plan = subscriptionplan.objects.get(title="Free Trial")
            #IF PLAN IS NOT CREATED
            if plan is None:
                return HttpResponse("Please Create Free Trial Plan")
            else:
                #ASSIGN USER WITH THE FREE PLAN
                user.plan = plan
                user.save()
            #GET CURRENT DATETIME
            timeNow = datetime.datetime.now(pytz.utc)
            #GET EXPIRY TIME
            timeThen = timeNow + datetime.timedelta(days=3)
            #CREATE TRIAL RECORD
            tryNow = trynowrecord(user=request.user, starttime=timeNow, endtime=timeThen)
            tryNow.save()
            redirectUrl = request.session['redirectUrl']
            if redirectUrl is not None:
                return redirect(redirectUrl)
            return redirect('/physics/')
    else:
        request.session['redirectUrl'] = "/finance/trynow/"
        return redirect('/accounts/login/')