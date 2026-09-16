from django.urls import path,include
from Admin import views 
app_name="Admin"

urlpatterns = [
  path('AdminHomePage/',views.homepage,name="homepage"),

  path('district/',views.district,name="district"),
  path('deletedistrict/<int:did>',views.deletedistrict,name="deletedistrict"),
  path('editdistrict/<int:eid>',views.editdistrict,name="editdistrict"),

  path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
  path('deleteAdmin/<int:did>',views.deleteAdmin,name="deleteAdmin"),
  path('editAdmin/<int:eid>',views.editAdmin,name="editAdmin"),

  path('Category/',views.Category,name="Category"),
  path('deleteCategory/<int:did>',views.deleteCategory,name="deleteCategory"),
  path('editCategory/<int:eid>',views.editCategory,name="editCategory"),

  path('Place/',views.Place,name="Place"),
  path('deletePlace/<int:did>',views.deletePlace,name="deletePlace"),
  path('editplace/<int:eid>',views.editplace,name="editplace"),
  

  path('SubCategory/',views.SubCategory,name="SubCategory"),
  path('deletesubcategory/<int:did>',views.deletesubcategory,name="deletesubcategory"),
  path('editSubCategory/<int:eid>',views.editsubcategory,name="editSubCategory"),


  path('Brand/',views.Brand,name="Brand"),
  path('deletebrand/<int:did>',views.deletebrand,name="deletebrand"),
  path('editbrand/<int:eid>',views.editbrand,name="editbrand"),



  path('Services/',views.Services,name="Services"),
  path('deleteservices/<int:did>',views.deleteservices,name="deleteservices"),
  path('editservices/<int:eid>',views.editservices,name="editservices"),


  path('ViewUser/',views.ViewUser,name="ViewUser"),
  

  path('ViewCompany/',views.ViewCompany,name="ViewCompany"),
  path('CompanyAccept/<int:aid>',views.CompanyAccept,name="CompanyAccept"),
  path('CompanyReject/<int:aid>',views.CompanyReject,name="CompanyReject"),



  path('ViewServiceProvide/',views.  ViewServiceProvider,name="ViewServiceProvider"),
  path('ServiceProviderAccept/<int:aid>',views.ServiceProviderAccept,name="ServiceProviderAccept"),
  path('ServiceProviderReject/<int:aid>',views.ServiceProviderReject,name="ServiceProviderReject"),



  path('ViewShop/',views.ViewShop,name="ViewShop"),
  path('ShopAccept/<int:aid>',views.ShopAccept,name="ShopAccept"),
  path('ShopReject/<int:aid>',views.ShopReject,name="ShopReject"),




  path('ViewComplaint/',views.ViewComplaint,name="ViewComplaint"),
  path('ComplaintReply/<int:id>/',views.ComplaintReply,name="ComplaintReply"),


  path('ViewFeedback/', views.ViewFeedback, name="ViewFeedback"),
  path('Logout/', views.Logout, name="Logout"),

  path('Banned/<int:bid>', views.Banned, name="Banned"),
  path('Unbanned/<int:bid>', views.Unbanned, name="Unbanned"),

  path('admin_report/', views.admin_report, name="admin_report"),

  path('Experience/', views.Experience, name="Experience"),
  path('deleteexperience/<int:id>/', views.deleteexperience, name='deleteexperience'),
  
  

   
]