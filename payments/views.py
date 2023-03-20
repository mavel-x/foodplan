import stripe

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


class PaymentPageView(TemplateView):
    template_name = 'payment.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = request.build_absolute_uri('/')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            product = stripe.Product.create(
                        name='Food Plan A',
                        description='Your food plan description',
                        )

            price = stripe.Price.create(
                    product=product.id,
                    unit_amount=20000,
                    currency='rub',
                    )
                    
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'profile/payment/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'profile/payment/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    }

                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
