# Generated by Django 4.2.2 on 2023-07-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0006_productfeedback_waiterfeedback_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Administratori', 'verbose_name_plural': 'Administratorët'},
        ),
        migrations.AddField(
            model_name='productfeedback',
            name='product_type',
            field=models.CharField(choices=[('F', 'Food'), ('B', 'Beverage')], default='F', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='ra_admin',
        ),
    ]