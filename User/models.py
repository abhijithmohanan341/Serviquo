from django.db import models
from Guest.models import *
from Company.models import *
from Shop.models import *

# Create your models here.


class tbl_companyservice(models.Model):
    companyservice_content=models.CharField(max_length=200)
    companyservice_date= models.DateTimeField()
    companyservice_status = models.IntegerField(default=0)
    companyservice_amount=models.IntegerField(null=True)
    companyservice_remark=models.CharField(max_length=500,null=True)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    company=models.ForeignKey(tbl_company, on_delete=models.CASCADE)
    technician=models.ForeignKey(tbl_technician, on_delete=models.CASCADE,null=True)
    




class tbl_servicerequest(models.Model):
    servicerequest_content=models.CharField(max_length=200)
    servicerequest_date= models.DateTimeField()
    servicerequest_amount=models.IntegerField(null=True)
    servicerequest_status = models.IntegerField(default=0)
    servicerequest_todate= models.DateField()
    servicerequest_remark=models.CharField(max_length=500,null=True)
    servicerequest_reject=models.CharField(max_length=1000,null=True)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    serviceprovider=models.ForeignKey(tbl_serviceprovider, on_delete=models.CASCADE)
    servicetype=models.ForeignKey(tbl_servicetype,on_delete=models.CASCADE)




class tbl_booking(models.Model):
    booking_date = models.DateTimeField(null=True, blank=True)
    booking_status=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    booking_address=models.CharField(max_length=600)
    booking_amount=models.FloatField(null=True)



class tbl_cart(models.Model):
    cart_status=models.IntegerField(default=0)
    cart_Qty=models.IntegerField(null=True)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    booking=models.ForeignKey(tbl_booking,on_delete=models.CASCADE)



class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=200)
    complaint_content=models.CharField(max_length=1000)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=500)
    complaint_status=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True)
    company=models.ForeignKey(tbl_company, on_delete=models.CASCADE,null=True)
    serviceprovider=models.ForeignKey(tbl_serviceprovider, on_delete=models.CASCADE,null=True)
    technician=models.ForeignKey(tbl_technician, on_delete=models.CASCADE,null=True)
    servicerequest = models.ForeignKey(tbl_servicerequest,on_delete=models.CASCADE,null=True, blank=True)
    companyservice = models.ForeignKey(tbl_companyservice,on_delete=models.CASCADE,null=True, blank=True)
    shop = models.ForeignKey(tbl_shop,on_delete=models.CASCADE,null=True, blank=True)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True)
    cart=models.ForeignKey(tbl_cart,on_delete=models.CASCADE,null=True)

    
    
    

class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=500)
    feedback_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True)



class tbl_rating(models.Model):
    datetime=models.DateField(auto_now_add=True)
    user_review=models.CharField(max_length=1000)
    rating_data=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True)
    companyservice=models.ForeignKey(tbl_companyservice, on_delete=models.CASCADE,null=True)
    servicerequest=models.ForeignKey(tbl_servicerequest, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True)












