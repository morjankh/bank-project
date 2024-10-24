# Generated by Django 5.1.2 on 2024-10-17 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_bankoperation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('transfer', 'Transfer')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='core.bankaccount')),
                ('destination_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transfers', to='core.bankaccount')),
            ],
        ),
        migrations.DeleteModel(
            name='BankOperation',
        ),
    ]