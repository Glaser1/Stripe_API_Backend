from items import views
from django.urls import path

app_name = "items"

urlpatterns = [
    path("item/buy/<int:item_id>/", views.create_checkout_session, name="create-checkout-session"),
    path("item/<int:item_id>/", views.get_item_info, name="item-info"),
    path("order/buy/<int:order_id>/", views.create_checkout_session_for_order, name="create-checkout-session-for-order"),
    path("order/<int:order_id>/", views.get_order_info, name="order-info"),
    path("success/", views.success_page, name="success"),
    path("cancel/", views.cancel_page, name="cancel"),
]
