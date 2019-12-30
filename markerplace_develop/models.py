from django.db import models


# Create your models here.

class User(models.Model):
    id = models.IntegerField('id', primary_key=True)
    user = models.CharField('user', max_length=20)
    password = models.CharField('password', max_length=30)

    class Meta:
        db_table = 'user'
