# Generated by Django 5.1.2 on 2024-10-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone_numb',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='adress',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]