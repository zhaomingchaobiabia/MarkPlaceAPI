# Generated by Django 2.2.7 on 2019-12-19 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('product_name', models.TextField(null=True, verbose_name='product_name')),
                ('product_fnac_id', models.CharField(max_length=50, null=True, verbose_name='product_fnac_id')),
                ('offer_fnac_id', models.CharField(max_length=50, null=True, verbose_name='offer_fnac_id')),
                ('offer_seller_id', models.CharField(max_length=50, null=True, verbose_name='offer_seller_id')),
                ('product_state', models.CharField(max_length=20, null=True, verbose_name='product_state')),
                ('price', models.CharField(max_length=20, null=True, verbose_name='price')),
                ('quantity', models.CharField(max_length=20, null=True, verbose_name='quantity')),
                ('description', models.TextField(null=True, verbose_name='description')),
                ('internal_comment', models.CharField(max_length=20, null=True, verbose_name='internal_comment')),
                ('product_url', models.TextField(null=True, verbose_name='product_url')),
                ('image', models.TextField(null=True, verbose_name='image')),
                ('nb_messages', models.CharField(max_length=20, null=True, verbose_name='nb_messages')),
                ('showcase', models.CharField(max_length=20, verbose_name='showcase')),
                ('is_shipping_free', models.CharField(max_length=20, verbose_name='is_shipping_free')),
                ('promotion', models.CharField(max_length=20, null=True, verbose_name='promotion')),
                ('starts_at', models.CharField(max_length=20, null=True, verbose_name='starts_at')),
                ('ends_at', models.CharField(max_length=20, null=True, verbose_name='ends_at')),
                ('pro_price', models.CharField(max_length=20, null=True, verbose_name='pro_price')),
                ('trigger_customer_type', models.CharField(max_length=20, null=True, verbose_name='trigger_customer_type')),
                ('type_label', models.CharField(max_length=20, null=True, verbose_name='type_label')),
            ],
            options={
                'db_table': 'offers',
            },
        ),
    ]