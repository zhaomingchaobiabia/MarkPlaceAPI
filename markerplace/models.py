from django.db import models


# Create your models here.


class Offers(models.Model):
    id = models.IntegerField('id', primary_key=True, auto_created=True)
    product_name = models.TextField('product_name', null=True, default='')
    product_fnac_id = models.CharField('product_fnac_id', max_length=50, null=True, default='')
    offer_fnac_id = models.CharField('offer_fnac_id', max_length=50, null=True, default='')
    offer_seller_id = models.CharField('offer_seller_id', max_length=50, null=True, default='')
    product_state = models.CharField('product_state', max_length=20, null=True, default='')
    price = models.CharField('price', max_length=20, null=True, default='')
    quantity = models.CharField('quantity', max_length=20, null=True, default='')
    description = models.TextField('description', null=True, default='')
    internal_comment = models.CharField('internal_comment', max_length=20, null=True, default='')
    product_url = models.TextField('product_url', null=True, default='')
    image = models.TextField('image', null=True, default='')
    nb_messages = models.CharField('nb_messages', max_length=20, null=True, default='')
    showcase = models.CharField('showcase', max_length=20, default='')
    is_shipping_free = models.CharField('is_shipping_free', max_length=20, default='')
    promotion = models.CharField('promotion', max_length=20, null=True, default='')
    starts_at = models.CharField('starts_at', max_length=20, null=True, default='')
    ends_at = models.CharField('ends_at', max_length=20, null=True, default='')
    pro_price = models.CharField('pro_price', max_length=20, null=True, default='')
    trigger_customer_type = models.CharField('trigger_customer_type', max_length=20, null=True, default='')
    type_label = models.CharField('type_label', max_length=20, null=True, default='')
    sort = models.CharField('sort', max_length=20, null=True)

    class Meta:
        db_table = 'offers'


class User(models.Model):
    id = models.IntegerField('id', primary_key=True, auto_created=True)
    user = models.CharField('user', max_length=30)
    password = models.CharField('password', max_length=5)

    class Meta:
        db_table = 'user'


class OfferOrder(models.Model):
    id = models.IntegerField('id', primary_key=True, auto_created=True)
    offer = models.CharField('offer', max_length=10)
    order = models.CharField('order', max_length=10)
    message = models.CharField('message', max_length=10)
    incident = models.CharField('incident', max_length=10)

    class Meta:
        db_table = 'offer_order_message_incident_num'
