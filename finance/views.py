from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
import stripe
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[
              'card',
            ],
            line_items=[
                {
                    'price_data':{
                        'currency':'inr',
                        'unit_amount' : 500,
                        'product_data':{
                            'name': 'Examination Fees',
                            'images' : ['http://127.0.0.1:8000/static/logos/logo.png'],
                        },
                    },
                    'quantity' : 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/finance/success/',
            cancel_url=YOUR_DOMAIN + '/finance/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

def success(request):
    return HttpResponse('Your payment was successfull')

def cancel(request):
    return redirect("finance/")