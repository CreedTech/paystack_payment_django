from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
from .forms import PaymentForm
from django.conf import settings
from .models import Payment

# Create your views here.

def initiate_payment(request) -> HttpResponse:
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})

def verify_payment(request, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification successful.')
    else:
        messages.error(request, 'Verification failed.')
    return redirect('initiate-payment')