from django.db import models


# Create your models here.


class Offers(models.Model):
    id = models.IntegerField('id', primary_key=True, auto_created=True)
    product_name = models.TextField('product_name', null=True)
    product_fnac_id = models.CharField('product_fnac_id', max_length=50, null=True)
    offer_fnac_id = models.CharField('offer_fnac_id', max_length=50, null=True)
    offer_seller_id = models.CharField('offer_seller_id', max_length=50, null=True)
    product_state = models.CharField('product_state', max_length=20, null=True)
    price = models.CharField('price', max_length=20, null=True)
    quantity = models.CharField('quantity', max_length=20, null=True)
    description = models.TextField('description', null=True)
    internal_comment = models.CharField('internal_comment',max_length=20, null=True)
    product_url = models.TextField('product_url', null=True)
    image = models.TextField('image', null=True)
    nb_messages = models.CharField('nb_messages', max_length=20, null=True)
    showcase = models.CharField('showcase', max_length=20)
    is_shipping_free = models.CharField('is_shipping_free', max_length=20)
    promotion = models.CharField('promotion', max_length=20, null=True)
    starts_at = models.CharField('starts_at', max_length=20, null=True)
    ends_at = models.CharField('ends_at', max_length=20, null=True)
    pro_price = models.CharField('pro_price', max_length=20, null=True)
    trigger_customer_type = models.CharField('trigger_customer_type', max_length=20, null=True)
    type_label = models.CharField('type_label', max_length=20, null=True)

    class Meta:
        db_table = 'offers'
