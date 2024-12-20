# Generated by Django 4.2.16 on 2024-12-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Credit Card', 'Credit Card'), ('Cash', 'Cash'), ('Check', 'Check'), ('Bank Transfer', 'Bank Transfer')], max_length=50),
        ),
    ]
