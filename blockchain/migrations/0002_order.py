# Generated by Django 3.2.2 on 2021-10-15 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('completed', models.BooleanField(default=False)),
                ('deposit_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='blockchain.useraddresses')),
            ],
        ),
    ]