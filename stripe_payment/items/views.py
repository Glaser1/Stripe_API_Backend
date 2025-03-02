import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from currency_converter import CurrencyConverter

from items.models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_order_total(order, target_currency=settings.DEFAULT_CURRENCY):
    """Считает промежуточную стоимость всех товаров в валюте по умолчанию."""

    total_sum = 0
    currency_converter = CurrencyConverter()

    for item in order.items.all():
        if item.currency != target_currency:
            converted_price = currency_converter.convert(item.price, item.currency, target_currency)
            total_sum += converted_price
        else:
            total_sum += item.price
    if order.tax:
        total_sum += total_sum * order.tax.percentage / 100

    if order.discounts:
        total_discount = sum(discount.percent_off for discount in order.discounts.all())
        total_discount = min(total_discount, 100)
        total_sum -= total_sum * total_discount / 100
    return int(total_sum / 100)


@require_GET
def get_order_info(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id)
    total_sum = calculate_order_total(order)
    return render(
        request,
        template_name="payment_intent.html",
        context={
            "order_items": order.items.all(),
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "order_id": order.id,
            "total_sum": total_sum,
            "currency": settings.DEFAULT_CURRENCY,
        },
    )


def get_order_info_for_intent(order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("discounts").select_related("tax"),
        pk=order_id,
    )
    total_sum = calculate_order_total(order)
    return {"amount": total_sum, "currency": settings.DEFAULT_CURRENCY}


def create_payment_intent_for_order(order_id):
    """Создает PaymentIntent на основе Order с товарами,"""
    """ для заказа с товарами в разных валютах в качестве дефолтной выбрана "USD"."""

    order_info = get_order_info_for_intent(order_id)
    payment_intent = stripe.PaymentIntent.create(
        amount=order_info["amount"],
        currency=order_info["currency"],
    )
    return payment_intent


@csrf_exempt
@require_GET
def secret(request, order_id):
    payment_intent = create_payment_intent_for_order(order_id)
    return JsonResponse({"client_secret": payment_intent.client_secret})
