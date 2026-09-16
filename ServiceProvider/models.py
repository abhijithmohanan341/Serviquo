from django.db import models
from Admin.models import *
from ServiceProvider.models import *
from Guest.models import *

# Create your models here.

class tbl_serviceproviderstype(models.Model):
    servicetype = models.ForeignKey(tbl_servicetype, on_delete=models.CASCADE)
    serviceprovider = models.ForeignKey(tbl_serviceprovider, on_delete=models.CASCADE)