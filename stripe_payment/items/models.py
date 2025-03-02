from django.db import models
from django.core.validators import MaxValueValidator


class Item(models.Model):
    CURRENCY_CHOICES = [("usd", "USD"), ("eur", "EUR")]
    name = models.CharField("Название", max_length=50, help_text="Укажите имя товара")
    description = models.CharField("Описание", max_length=200, help_text="Введите описание товара")
    price = models.PositiveIntegerField("Цена", help_text="Укажите цену в центах")
    currency = models.CharField(
        "Валюта", max_length=3, default="usd", help_text="Укажите валюту в формате ISO 4217 (напр.: 'usd')"
    )

    def save(self, *args, **kwargs):
        self.currency = self.currency.lower()
        super().save(self, *args, **kwargs)

    def __str__(self):
        return f"Item: {self.name}"

    def __repr__(self):
        return f"Экземпляр {self.__class__.__name__}:  name={self.name}, id={self.id}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discounts = models.ManyToManyField("Discount")
    tax = models.ForeignKey("Tax", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def __repr__(self):
        return f"Экземпляр {self.__class__.__name__}: id={self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Tax(models.Model):
    name = models.CharField("Название", max_length=100)
    percentage = models.IntegerField("Налог", help_text="Укажите налог в процентах")

    def __str__(self):
        return f"Tax #{self.id}"

    def __repr__(self):
        return f"Экземпляр {self.__class__.__name__}: id={self.id}"

    class Meta:
        verbose_name = "Налоги"
        verbose_name_plural = "Налоги"


class Discount(models.Model):
    percent_off = models.IntegerField(
        "Скидка", help_text="Укажите скидку в процентах", validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return f"Discount #{self.id}"

    def __repr__(self):
        return f"Экземпляр {self.__class__.__name__}: id={self.id}"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидка"
