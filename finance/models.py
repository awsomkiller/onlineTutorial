from django.db import models
from django.db.models.deletion import PROTECT
from accounts.models import User

# Create your models here.
class payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=PROTECT)
    amount = models.CharField(max_length=100, default="500")
    time = models.DateTimeField(auto_now_add=True)