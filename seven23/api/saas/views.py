"""
    Views for api/va/transactions
"""
import stripe
import json
import os
import markdown2
import urllib.parse
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from seven23 import settings
from seven23.models.profile.models import Profile
from seven23.models.terms.models import TermsAndConditions

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET', 'DELETE'])
def StripeSubscriptions(request):
    stripe_customer_id = None
    try:
        stripe_customer_id = request.user.profile.stripe_customer_id
    except:
        pass

    if request.method == 'GET':
        products = stripe.Product.list(active=True)
        prices = stripe.Price.list(product=products.data[0].id)

        if not stripe_customer_id:
            j = json.dumps({
                'products': products,
                'prices': stripe.Price.list(product=products.data[0].id)
            }, separators=(',', ':'))
        else:
            subscriptions = stripe.Subscription.list(customer=stripe_customer_id)
            paymentMethod = None
            if len(subscriptions.data):
                paymentMethod = stripe.PaymentMethod.retrieve(subscriptions.data[0].default_payment_method)
            j = json.dumps({
                'subscriptions': subscriptions,
                'invoices': stripe.Invoice.list(customer=stripe_customer_id),
                'products': products,
                'prices': stripe.Price.list(product=products.data[0].id),
                'paymentMethod': paymentMethod
            }, separators=(',', ':'))

        return HttpResponse(j, content_type='application/json')

    elif request.method == 'DELETE':

        if not stripe_customer_id:
            return HttpResponse(status=400)

        subscription = stripe.Subscription.list(customer=stripe_customer_id)
        stripe.Subscription.delete(subscription.data[0])
        return Response(status=status.HTTP_200_OK)
    else:
        return HttpResponse(status=400)



@api_view(['GET'])
def StripeGenerateSession(request):
    stripe_customer_id = request.user.profile.stripe_customer_id

    text_rate = stripe.TaxRate.list().data[0].id;

    timestamp_now = int(time.mktime(datetime.datetime.now().timetuple()))
    timestamp_valid_until = int(time.mktime(request.user.profile.valid_until.timetuple()))

    trial_period_days = None
    if timestamp_now < timestamp_valid_until:
        trial_period_days = int((timestamp_valid_until - timestamp_now) / 86400)
        if trial_period_days < 1:
            trial_period_days = None


    session = stripe.checkout.Session.create(
      customer=request.user.profile.stripe_customer_id,
      customer_email=request.user.email if not stripe_customer_id else None,
      payment_method_types=['card'],
      allow_promotion_codes=True,
      line_items=[{
        'price': request.GET.get("price_id"),
        'quantity': 1
      }],
      mode='subscription',
      # success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
      # cancel_url='https://example.com/cancel',
      success_url=urllib.parse.urljoin(request.GET.get("success_url"), 'success'),
      cancel_url=request.GET.get("cancel_url"),
      subscription_data={
        'default_tax_rates': [text_rate],
        'trial_period_days': trial_period_days
      }
    )

    request.user.profile.stripe_session_id = session.id
    request.user.profile.save()

    j = json.dumps({
        'session_id': session
    }, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def StripeWebhook(request):
    payload = request.body
    try:
        event = stripe.Event.construct_from(
          json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    # Handle the event

    if event.type == 'checkout.session.completed':
        checkout = event.data.object # contains a stripe.PaymentIntent

        profile = Profile.objects.get(stripe_session_id=checkout.id)
        if profile:
            profile.stripe_customer_id = checkout.customer
            profile.save()
            return Response(status=status.HTTP_200_OK)

    elif event.type == 'invoice.paid':
        invoice = event.data.object

        profile = Profile.objects.get(stripe_customer_id=invoice.customer)
        profile.valid_until = datetime.datetime.fromtimestamp(invoice.lines.data[0].period.end)
        profile.save()
        return Response(status=status.HTTP_200_OK)
    else:
        # Unexpected event type
        return HttpResponse(status=400)
    return Response(status=status.HTTP_200_OK)