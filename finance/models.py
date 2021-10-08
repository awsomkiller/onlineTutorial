from django.db import models
from accounts.models import User, subscriptionplan

# Create your models here.

#PAYMENT RECORD.
class payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(subscriptionplan, on_delete=models.PROTECT, null=True)
    amount = models.CharField(max_length=10)
    time = models.DateTimeField()

#PAYMENT ATTEMPT RECORD.
class checkoutrecord(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(subscriptionplan, on_delete=models.PROTECT)
    amount = models.CharField(max_length=10)
    time = models.DateTimeField()
    status = models.CharField(max_length=15)
    isactive = models.BooleanField(default=True)