# Generated by Django 4.0.5 on 2022-07-12 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kodius', '0003_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]