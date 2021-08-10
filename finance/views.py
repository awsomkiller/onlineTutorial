# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.


from finance.models import payment
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import stripe
from accounts.models import User


stripe.api_key = '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'

def create_checkout_session(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                'name': 'Examination Fees',
                },
                'unit_amount': 50000,
            },
            'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/finance/success',
            cancel_url='https://127.0.0.1:8000/finance/cancel',
            )
            return redirect(session.url, code=303)
        else:
            return HttpResponse("Session closed")
    else:
        return redirect('/')


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
