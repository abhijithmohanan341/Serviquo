from django.urls import path,include
from User import views 
app_name="User"

urlpatterns = [
    path('UserHomePage/',views.homepage,name="homepage"),
    path('MyProfile/',views.myprofile,name="myprofile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path("EditPhoto/", views.EditPhoto, name="EditPhoto"),


    path('ViewCompany/',views.ViewCompany,name="ViewCompany"),
    path('CompanyRequest/<int:id>',views.CompanyRequest,name="CompanyRequest"),
    path('MyCompanyRequest/',views.MyCompanyRequest,name="MyCompanyRequest"),
    path('cancel-company-service/<int:cid>/', views.CancelCompanyServiceRequest, name='CancelCompanyServiceRequest'),



    path('ViewServiceProvider/',views.ViewServiceProvider,name="ViewServiceProvider"),
    path('ServiceProviderRequest/<int:id>',views.ServiceProviderRequest,name="ServiceProviderRequest"),
    path('MyServiceRequest/',views.MyServiceRequest,name="MyServiceRequest"),
    path('cancelservicerequest/<int:did>/', views.CancelServiceRequest, name='CancelServiceRequest'),
    path('ServicePaymentComplete/<int:aid>',views.ServicePaymentComplete,name="ServicePaymentComplete"),
    path('CompanyPaymentComplete/<int:aid>',views.CompanyPaymentComplete,name="CompanyPaymentComplete"),
    path('ShopPaymentComplete/<int:aid>',views.ShopPaymentComplete,name="ShopPaymentComplete"),



    path('Complaint/',views.Complaint,name="Complaint"),
    path('DeleteComplaint/<int:did>',views.DeleteComplaint,name="DeleteComplaint"),
    path('EditComplaint/<int:eid>',views.EditComplaint,name="EditComplaint"),


    path('CompanyComplaint/<int:csid>',views.CompanyComplaint,name="CompanyComplaint"),
    path('ServiceProviderComplaint/<int:sid>',views.ServiceProviderComplaint,name="ServiceProviderComplaint"),
    path('TechnicianComplaint/<int:tid>',views.TechnicianComplaint,name="TechnicianComplaint"),



    path('Feedback/',views.Feedback,name="Feedback"),
    path('DeleteFeedback/<int:did>',views.DeleteFeedback,name="DeleteFeedback"),
    path('EditFeedback/<int:eid>',views.EditFeedback,name="EditFeedback"),


    path('ViewShop/',views.ViewShop,name="ViewShop"),
    path('viewproduct/<int:shopid>/', views.ViewProduct, name="ViewProduct"),
    path('ajaxProductCategory/<int:shopid>/', views.ajaxProductCategory, name="ajaxProductCategory"),


    path("companypayment/<int:id>",views.companypayment,name="companypayment"),
    path("servicepayment/<int:id>",views.servicepayment,name="servicepayment"),
    path("shoppayment/<int:id>",views.shoppayment,name="shoppayment"),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),


    path('AddtoCart/<int:pid>/<int:shopid>/',views.AddtoCart,name='AddtoCart'),
    path('MyBooking/',views.MyBooking, name='MyBooking'),
    path('OrderCancel/<int:bid>/', views.OrderCancel, name='OrderCancel'),
    path('Mycart/',views.Mycart, name='Mycart'),   
    path("DelCart/<int:did>", views.DelCart,name="delcart"),
    path("CartQty/", views.CartQty,name="cartqty"),
    path('BuyNow/<int:pid>/', views.BuyNow, name='BuyNowPage'),


    path('ajaxService/',views.ajaxService,name="ajaxService"),
    path('ajaxCompanyBrand/', views.ajaxCompanyBrand, name='ajaxCompanyBrand'),

    path('ProductComplaint/<int:pid>/<int:cid>/',views.ProductComplaint,name="ProductComplaint"),
    path('EditProductComplaint/<int:cid>/', views.EditProductComplaint, name='EditProductComplaint'),
    path('DeleteProductComplaint/<int:did>/', views.DeleteProductComplaint, name='DeleteProductComplaint'),

    path('Logout/', views.Logout, name="Logout"),

    path('productrating/<int:mid>/',views.productrating,name="productrating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),


    path('servicerating/<int:mid>/',views.servicerating,name="servicerating"),  
    path('serviceajaxstar/',views.serviceajaxstar,name="serviceajaxstar"),
    path('servicestarrating/',views.servicestarrating,name="servicestarrating"),


    path('companyrating/<int:mid>/',views.companyrating,name="companyrating"),  
    path('companyajaxstar/',views.companyajaxstar,name="companyajaxstar"),
    path('companystarrating/',views.companystarrating,name="companystarrating"),
    

    path('ReServiceRequest/<int:rid>/', views.ReServiceRequest, name="ReServiceRequest"),
    path('ReCompanyServiceRequest/<int:rid>/', views.ReCompanyServiceRequest, name="ReCompanyServiceRequest"),

    path('UserBill/<int:bid>/', views.UserBill, name="UserBill"),

    path('ServiceBill/<int:rid>/', views.ServiceBill, name="ServiceBill"),

    path('CompanyServiceBill/<int:cid>/', views.CompanyServiceBill, name="CompanyServiceBill"),



]