# Generated by Django 4.2.2 on 2025-05-24 16:04

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teknopark_app', '0007_meetingtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='talep_edilen_yatirim',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Girişimci isen, talep ettiğin yatırım miktarı ($)', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
        migrations.AddField(
            model_name='customuser',
            name='yatirim_miktari',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Yatırımcı isen, yatırım yapmayı düşündüğün miktar ($)', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
    ]
