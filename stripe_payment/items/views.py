import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from items.models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def success_page(request):
    return render(request, template_name="success.html")


def cancel_page(request):
    return render(request, template_name="cancel.html")


def create_stripe_product_and_price(item_id):
    item = get_object_or_404(Item, id=item_id)
    price = stripe.Price.create(
        currency=item.currency,
        product_data={"name": item.name},
        unit_amount=item.price,
    )
    return price


def create_stripe_order_list(order):
    order_list = []

    order_tax = order.tax

    if order_tax:
        tax_rate = stripe.TaxRate.create(
            display_name=order_tax.name,
            percentage=order_tax.percentage,
            inclusive=False,
        )
    for item in order.items.all():
        price = stripe.Price.create(
            currency=item.currency,
            product_data={"name": item.name},
            unit_amount=item.price,
        )
        order_list.append({"price": price.id, "quantity": 1, "tax_rates": [tax_rate.id] if order_tax else []})

    return order_list


@require_GET
def create_checkout_session_for_order(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items").prefetch_related("discounts"), id=order_id)
    order_list = create_stripe_order_list(order)

    coupons_ids = []

    if order.discounts.exists():
        for discount in order.discounts.all():
            coupon = stripe.Coupon.create(percent_off=discount.percent_off)
            coupons_ids.append(coupon.id)

    session = stripe.checkout.Session.create(
        line_items=order_list,
        mode="payment",
        success_url=settings.APP_DOMAIN + "/success/",
        cancel_url=settings.APP_DOMAIN + "/cancel/",
        discounts=[{"coupon": v} for v in coupons_ids],
    )

    return JsonResponse({"id": session.id})


@require_GET
def create_checkout_session(request, item_id):
    price = create_stripe_product_and_price(item_id)
    session = stripe.checkout.Session.create(
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url=settings.APP_DOMAIN + "/success/",
        cancel_url=settings.APP_DOMAIN + "/cancel/",
    )
    return JsonResponse({"id": session.id})


@require_GET
def get_item_info(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(
        request, template_name="item.html", context={"item": item, "stripe_public_key": settings.STRIPE_PUBLIC_KEY}
    )


@require_GET
def get_order_info(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id)
    return render(
        request,
        template_name="order.html",
        context={
            "order_id": order.id,
            "order_items": order.items.all(),
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        },
    )
