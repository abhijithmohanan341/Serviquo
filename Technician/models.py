from django.db import models
from Company.models import *

# Create your models here.


class tbl_technicianleave(models.Model):
    leave_fromdate=models.DateField()
    leave_todate=models.DateField()
    leave_reason=models.CharField(max_length=200)
    leave_status=models.IntegerField(default=0)
    applied_date=models.DateField(auto_now_add=True)
    technician=models.ForeignKey(tbl_technician, on_delete=models.CASCADE)












    