from django.urls import path,include
from Company import views 
app_name="Company"

urlpatterns = [
    path('CompanyHomePage/',views.homepage,name="homepage"),
    path('CompanyProfile/',views.CompanyProfile,name="CompanyProfile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path("EditPhoto/<int:cid>/", views.EditPhoto, name="EditPhoto"),


    path('TechnicianRegistration/',views.TechnicianRegistration,name="TechnicianRegistration"),
    path('deleteTechnician/<int:did>',views.deleteTechnician,name="deleteTechnician"),
    path('editTechnician/<int:eid>',views.editTechnician,name="editTechnician"),

    path('ViewRequest/',views.ViewRequest,name="ViewRequest"),
    path('CancelCompanyServiceRequest/<int:did>/', views.CancelCompanyServiceRequest, name='CancelCompanyServiceRequest'),
    path('CompanyServiceAccept/<int:aid>/', views.CompanyServiceAccept, name="CompanyServiceAccept"),
    path('CompanyServiceReject/<int:aid>/', views.CompanyServiceReject, name="CompanyServiceReject"),

    
    path('TechnicianAssign/',views.TechnicianAssign,name="TechnicianAssign"),
    path('Assign/<int:rid>/',views.Assign,name="Assign"),


    path('Complaint/',views.Complaint,name="Complaint"),
    path('ViewComplaint/',views.ViewComplaint,name="ViewComplaint"),
    path('ComplaintReply/<int:id>/',views.ComplaintReply,name="ComplaintReply"),
    
    path('DeleteComplaint/<int:did>',views.DeleteComplaint,name="DeleteComplaint"),
    path('EditComplaint/<int:eid>',views.EditComplaint,name="EditComplaint"),


    path('ViewUserComplaint/<int:cid>',views.ViewUserComplaint,name="ViewUserComplaint"),
    path('ComplaintReply/<int:id>/',views.ComplaintReply,name="ComplaintReply"),
    path('UserComplaintReply/<int:id>/',views.UserComplaintReply,name="UserComplaintReply"),



    path('CompanyPaymentComplete/<int:aid>',views.CompanyPaymentComplete,name="CompanyPaymentComplete"),



    path('viewleaverequest/',views.ViewLeaveRequest, name="ViewLeaveRequest"),
    path('Accept/<int:id>/',views.AcceptLeave, name="AcceptLeave"),
    path('Aeject/<int:id>/',views.RejectLeave, name="RejectLeave"),


    path('Logout/', views.Logout, name="Logout"),

    path('ViewCompanyServiceRating/<int:cid>/', views.ViewCompanyServiceRating, name='ViewCompanyServiceRating'),

    path('company_revenue_report/', views.company_revenue_report, name="company_revenue_report"),


]