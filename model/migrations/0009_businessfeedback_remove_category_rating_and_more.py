# Generated by Django 4.2.2 on 2023-07-06 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0008_category_menu_products_alter_acactionlogger_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Data e krijimit')),
                ('date_last_updated', models.DateTimeField(auto_now=True, verbose_name='Data e modifikimit')),
                ('rating', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Vlerësimi për biznesin',
                'verbose_name_plural': 'Vlerësimet për biznesin',
                'db_table': 'si_business_feedback',
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='products',
            name='rating',
        ),
        migrations.AddField(
            model_name='category',
            name='rating',
            field=models.ManyToManyField(related_name='category_ratings', to='model.businessfeedback'),
        ),
        migrations.AddField(
            model_name='products',
            name='rating',
            field=models.ManyToManyField(related_name='product_ratings', to='model.businessfeedback'),
        ),
    ]
