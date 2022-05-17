from finance.models import payment, checkoutrecord, trynowrecord
from accounts.models import otpModel
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
import random
import urllib.request
import razorpay

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

if settings.DEBUG:
    success=env('TEST_SUCCESS')
    cancel=env('TEST_CANCEL')
    stripe.api_key = env('STRIPE_TEST_KEY')
    endpoint_secret = env('ENDPOINTTEST_SECRET')
    #razorpay settings
    YOUR_ID = env('YOUR_TESTID')
    YOUR_SECRET = env('YOUR_TESTSECRET')
else:
    stripe.api_key = env('STRIPE_LIVE_KEY')
    success=env('SUCCESS')
    cancel=env('CANCEL')
    endpoint_secret = env('ENDPOINT_SECRET')
    #razorpay settings
    YOUR_ID = env('YOUR_LIVEID')
    YOUR_SECRET = env('YOUR_LIVESECRET')

def create_checkout_session(request):
    #CHECK USER AUTHENTICATION
    if request.user.is_authenticated:
        #CHECK SESSION TIME
        checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
        checkoutobj = checkoutobj[0]
        timeNow = datetime.datetime.now()
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
                checkoutobj.stripe_payment_intent = session['payment_intent']
                checkoutobj.save()
                return redirect(session.url, code=303)
            else:
                return HttpResponse("INVALID REQUEST")
        else:
            return HttpResponse("Session time is out, please try again.")
    else:
        request.session['redirectUrl'] = "/finance/create-checkout-session/"
        return redirect('/accounts/login/')

# @csrf_exempt
# def razorwebhook(request):
#     print("got request")
#     return redirect('/')

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

  # Handle the event
  if event.type == 'checkout.session.completed':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    print('PaymentIntent was successful!')
    session = event['data']['object']
    if(session['status']=="complete"):
        checkoutobj = checkoutrecord.objects.get(stripe_payment_intent=session['payment_intent'])
        user = checkoutobj.user
        checkoutobj.isactive=False
        checkoutobj.status = "success"
        checkoutobj.save()
        paymentRecord = payment(user = user, plan = checkoutobj.plan, amount=checkoutobj.amount)
        paymentRecord.save()
        user.plan = checkoutobj.plan
        user.save()
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    print('PaymentMethod was attached to a Customer!')
  # ... handle other event types
  else:
    print('Unhandled event type {}'.format(event.type))

  return HttpResponse(status=200)

def success_url(request):
    if request.method=="POST":
        if 'razorpay_order_id' in request.POST:
            orderId = request.POST['razorpay_order_id']
            checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True, stripe_payment_intent=orderId)
            if checkoutobj is None:
                return HttpResponse("Error occured during payment, Contact: Site admin error code :103")
            checkoutobj = checkoutobj[0]
            user = checkoutobj.user
            checkoutobj.isactive=False
            checkoutobj.status = "success"
            checkoutobj.save()
            paymentRecord = payment(user = user, plan = checkoutobj.plan, amount=checkoutobj.amount)
            paymentRecord.save()
            user.plan = checkoutobj.plan
            user.save()
            return render(request, 'successPayment.html', {'name':user.name, 'plan':user.plan, 'amount':checkoutobj.amount })
        return HttpResponse('Error occured, If payment deducted contact site admin')
    else:
        return redirect('/')

def cancel_url(request):
    checkoutobj = checkoutrecord.objects.filter(user=request.user, isActive=True)
    checkoutobj = checkoutobj[0]
    checkoutobj.status = "cancel"
    checkoutobj.isActive = False
    checkoutobj.save()
    return redirect('/finance/user-plan/')

def checkout(request):
    #CHECK USER AUTHENTICATION
    if request.user.is_authenticated:
        #CHECK SESSION TIME
        checkoutobj = checkoutrecord.objects.filter(user=request.user, isactive=True)
        checkoutobj = checkoutobj[0]
        timeNow = datetime.datetime.now()
        dt = checkoutobj.time
        dt.replace(tzinfo=None)
        timedifference =  timeNow - dt
        duration = timedifference.total_seconds()
        duration = duration / 60
        #IF DURATION IS LESS 10 MINS
        amount =  int(checkoutobj.amount)
        amount = amount*100
        Data = {
                'amount': amount,
                'currency':"INR",
                'notes':{
                    "id":checkoutobj.id,
                }
        }
        client = razorpay.Client(auth=(YOUR_ID,YOUR_SECRET))
        client.order.create(data=Data)
        dataobj = client.order.all('authorized')
        orderobj = None
        for items in dataobj['items']:
            temp = items['notes']
            if temp['id'] == checkoutobj.id:
                orderobj= items
                break
        if orderobj == None:
            return HttpResponse("Error occured inform to site admin. error :101")
        checkoutobj.stripe_payment_intent=orderobj['id']
        checkoutobj.save()
        name = request.user.name
        email = request.user.email
        plan = checkoutobj.plan
        plan = plan.title
        contact = request.user.mobile
        orderid = orderobj['id']
        return render(request, 'checkout.html',{'name': name, 'amount':amount, 'email': email, 'plan': plan, "checkout": checkoutobj, "apiid":YOUR_ID, 'contact':contact, 'orderid':orderid })
    request.session['redirectUrl'] = "/finance/user-plan/"
    return redirect('/accounts/login/')

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
                    plan.normal_cost = str(int(plan.normal_cost) )
                    plan.discounted_price = str(int(plan.discounted_price))
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
                existingcheckout = checkoutrecord.objects.filter(user=request.user)
                existingcheckout = existingcheckout[0]
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
                        planprice = int(new_plan.discounted_price)
                    else:
                        #OUTSIDER
                        planprice = int(new_plan.normal_cost)

                    #CHECK NEW PLAN IS GREATER THEN ACTIVE PLAN
                    if planprice < 0:
                        HttpResponse('Invalid Response')
                    else:
                        #ADDING PLAN CHANGE CHARGERS OF 100
                        planprice = planprice
                    checkOutObject = checkoutrecord(user=request.user, plan=new_plan, amount=planprice, time=timenow, status="attempting")
                    checkOutObject.save()
            return redirect('/finance/checkout/')
    else:
        request.session['redirectUrl'] = "/finance/user-plan/select-plan=" + str(planid) + "/"
        return redirect('/accounts/login/')
           
def try_now(request):
    #CHECK USER IS AUTHENTICATED
    if request.user.is_authenticated:
        if request.user.is_verified:
            #CHECK USER HAS ALREADY ACTIVATED TO FREE TRIAL.
            if trynowrecord.objects.filter(user=request.user, active=True).exists():
                tryNow = trynowrecord.objects.get(user=request.user, active=True)
                timeNow = datetime.datetime.now(pytz.utc)
                #CHECK TRIAL EXPIRY.
                if(timeNow>tryNow.endtime):
                    tryNow.active = False
                    tryNow.save()
                #REDIRECT TO OPT A NEW PLAN
                return redirect('/finance/user-plan/')
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
                if 'redirectUrl' in request.session:
                    redirectUrl = request.session['redirectUrl']
                    return redirect(redirectUrl)
                return redirect('/physics/')
        else:
            mobileNumber = request.user.mobile
            fullName = request.user.name
            request.session['otpid']=mobileNumber
            n = random.randint(10000, 99999)
            name = fullName.split()
            try:
                otpObj = otpModel.objects.get(phonenumber=mobileNumber)
                otpObj.otp = n
                otpObj.current_time = datetime.datetime.now()
            except otpModel.DoesNotExist:
                otpObj = otpModel(phonenumber=mobileNumber, otp=n, current_time=datetime.utcnow() )
            otpObj.save()
            uphonenum = str(mobileNumber)
            un = str(n)
            url1 = "http://smsshoot.in/http-tokenkeyapi.php?authentic-key=3739726b656475763934321627812964&senderid=ABHINM&route=2&number="+uphonenum+"&message=Dear%20"
            url2 = name[0]+"%20OTP%20to%20login%20into%20Rkeduv(account)%20is%20"+un+".%20Do%20not%20Share%20with%20anyone.%20-Rkeduv%20abhinm&templateid=1707162694588395444"
            url1 = url1 + url2
            request_url = urllib.request.urlopen(url1)
            return redirect("/accounts/activate/")
    else:
        request.session['redirectUrl'] = "/finance/trynow/"
        return redirect('/accounts/login/')