from django.urls import path,include
from ServiceProvider import views 
app_name="ServiceProvider"

urlpatterns = [
    path('ServiceProviderHomePage/',views.homepage,name="homepage"),
    path('ServiceProviderProfile/',views.ServiceProviderProfile,name="ServiceProviderProfile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path("EditPhoto/<int:sid>/", views.EditPhoto, name="EditPhoto"),

    path('MyServices/', views.MyServices, name="MyServices"),
    path('deleteserviceproviderstype/<int:did>',views.deleteserviceproviderstype,name="deleteserviceproviderstype"),
    path('editserviceproviderstype/<int:eid>',views.editserviceproviderstype,name="editserviceproviderstype"),


    path('MyServiceRequest/',views.MyServiceRequest,name="MyServiceRequest"),
    path('userdetails/<int:id>/', views.UserDetails, name='UserDetails'),
    path('ServiceAccept/<int:aid>',views.ServiceAccept,name="ServiceAccept"),
    path('ServiceReject/<int:aid>',views.ServiceReject,name="ServiceReject"),
    path('ServiceStart/<int:aid>',views.ServiceStart,name="ServiceStart"),
    path('ServiceProgress/<int:aid>',views.ServiceProgress,name="ServiceProgress"),
    path('ServiceEnd/<int:aid>',views.ServiceEnd,name="ServiceEnd"),
    path('cancelservicerequest/<int:did>/', views.CancelServiceRequest, name='CancelServiceRequest'),



    path('Complaint/',views.Complaint,name="Complaint"),
    path('DeleteComplaint/<int:did>',views.DeleteComplaint,name="DeleteComplaint"),
    path('EditComplaint/<int:eid>',views.EditComplaint,name="EditComplaint"),

    path('ViewUserComplaint/<int:sid>/',views.ViewUserComplaint,name="ViewUserComplaint"),
    path('ComplaintReply/<int:id>/',views.ComplaintReply,name="ComplaintReply"),


    path('Amount/<int:aid>',views.Amount,name="Amount"),
    path('ServicePaymentComplete/<int:aid>',views.ServicePaymentComplete,name="ServicePaymentComplete"),


    path('Logout/', views.Logout, name="Logout"),


    path('ViewServiceRating/<int:sid>/', views.ViewServiceRating, name='ViewServiceRating'),

    path('ServiceRemark/<int:id>/',views.ServiceRemark,name="ServiceRemark"),

    path('serviceprovider_revenue_report/', views.serviceprovider_revenue_report, name="serviceprovider_revenue_report"),

    path('ServiceRejectReply/<int:id>/',views.ServiceRejectReply,name="ServiceRejectReply"),




]