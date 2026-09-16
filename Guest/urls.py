from django.urls import path,include
from Guest import views 
app_name="Guest"

urlpatterns = [
  path('UserRegistration/',views.UserRegistration,name="UserRegistration"),
  path('CompanyRegistration/',views.CompanyRegistration,name="CompanyRegistration"),
  path('ServiceProviderRegistration/',views.ServiceProviderRegistration,name="ServiceProviderRegistration"),
  path('ShopRegistration/',views.ShopRegistration,name="ShopRegistration"),
  path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
  path('Login/',views.Login,name="Login"),

  path('',views.Index,name="Index"),

  path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
  path('otp/',views.otp,name="otp"),
  path('newpass/',views.newpass,name="newpass"),
  path('allregistrations/',views.allregistrations,name="allregistrations"),
  path('AjaxEmailCheck/', views.AjaxEmailCheck, name="AjaxEmailCheck"),
  


]