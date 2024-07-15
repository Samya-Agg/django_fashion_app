# Generated by Django 4.2.11 on 2024-07-14 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0007_alter_outfit_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_outfits', to=settings.AUTH_USER_MODEL),
        ),
    ]
