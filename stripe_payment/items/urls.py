from items import views
from django.urls import path

app_name = "items"

urlpatterns = [
    path("order/<int:order_id>/", views.get_order_info, name="get_order_info"),
    path("create-payment-intent/<int:order_id>", views.secret, name="create_payment_intent"),
]
