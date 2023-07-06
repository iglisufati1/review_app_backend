# Generated by Django 4.2.2 on 2023-07-06 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0007_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Data e krijimit')),
                ('date_last_updated', models.DateTimeField(auto_now=True, verbose_name='Data e modifikimit')),
                ('name', models.CharField(max_length=20)),
                ('rating', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategortë',
                'db_table': 'si_category',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Data e krijimit')),
                ('date_last_updated', models.DateTimeField(auto_now=True, verbose_name='Data e modifikimit')),
            ],
            options={
                'verbose_name': 'Menuja',
                'verbose_name_plural': 'Menutë',
                'db_table': 'si_menu',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Data e krijimit')),
                ('date_last_updated', models.DateTimeField(auto_now=True, verbose_name='Data e modifikimit')),
                ('name', models.CharField(max_length=20)),
                ('rating', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='model.category')),
            ],
            options={
                'verbose_name': 'Produkti',
                'verbose_name_plural': 'Produktet',
                'db_table': 'si_product',
            },
        ),
        migrations.AlterModelTable(
            name='acactionlogger',
            table='si_action_logger',
        ),
        migrations.AlterModelTable(
            name='business',
            table='si_business',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='si_admin',
        ),
        migrations.AlterModelTable(
            name='waiter',
            table='si_waiter',
        ),
        migrations.AlterModelTable(
            name='waiterfeedback',
            table='si_waiter_feedback',
        ),
        migrations.DeleteModel(
            name='ProductFeedback',
        ),
        migrations.AddField(
            model_name='menu',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='model.business'),
        ),
        migrations.AddField(
            model_name='category',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='model.menu'),
        ),
    ]