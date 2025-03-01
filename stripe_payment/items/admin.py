from django.contrib import admin

from .models import Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "currency")
    search_fields = (
        "name",
        "description",
    )
    list_filter = ("currency",)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "id",
        "total_sum",
    )

    def total_sum(self, obj):
        return sum(item.price for item in obj.items.all())

    total_sum.short_description = "Сумма заказа"

    def order(self, obj):
        return str(obj)

    order.short_description = "Заказ"


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
