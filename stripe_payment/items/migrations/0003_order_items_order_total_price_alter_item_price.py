# Generated by Django 5.1.6 on 2025-03-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0002_item_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="items",
            field=models.ManyToManyField(to="items.item"),
        ),
        migrations.AddField(
            model_name="order",
            name="total_price",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.PositiveIntegerField(
                help_text="Укажите цену в центах", verbose_name="Цена"
            ),
        ),
    ]
