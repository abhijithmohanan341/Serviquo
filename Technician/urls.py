from django.urls import path,include
from Technician import views 
app_name="Technician"

urlpatterns = [
     path('TechnicianHomePage/',views.homepage,name="homepage"),
     path('TechnicianProfile/',views.TechnicianProfile,name="TechnicianProfile"),
     path('EditProfile/',views.EditProfile,name="EditProfile"),
     path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
     path("EditPhoto/<int:tid>/", views.EditPhoto, name="EditPhoto"),


     path("MyRequest/", views.MyRequest, name="MyRequest"),
     path('userdetails/<int:id>/', views.UserDetails, name='UserDetails'),
     



     path('Complaint/',views.Complaint,name="Complaint"),
     path('DeleteComplaint/<int:did>',views.DeleteComplaint,name="DeleteComplaint"),
     path('EditComplaint/<int:eid>',views.EditComplaint,name="EditComplaint"),

     
     path('ServiceStart/<int:aid>',views.ServiceStart,name="ServiceStart"),
     path('ServiceProgress/<int:aid>',views.ServiceProgress,name="ServiceProgress"),
     path('ServiceEnd/<int:aid>',views.ServiceEnd,name="ServiceEnd"),


     path('Amount/<int:aid>',views.Amount,name="Amount"),
     path('CompanyPaymentComplete/<int:aid>',views.CompanyPaymentComplete,name="CompanyPaymentComplete"),



     path('LeaveRequest/',views.LeaveRequest,name="LeaveRequest"),
     path("deleteleave/<int:did>/",views.DeleteLeave, name="DeleteLeave"),


     path('Logout/', views.Logout, name="Logout"),



     path('ServiceRemark/<int:id>/',views.ServiceRemark,name="ServiceRemark"),

     path('revenue_report/',views.technician_revenue_report,name='technician_revenue_report'),



]