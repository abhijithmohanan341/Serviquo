from django.urls import path,include
from Shop import views 
app_name="Shop"

urlpatterns = [

path('ShopHomePage/',views.homepage,name="homepage"),
path('ShopProfile/',views.ShopProfile,name="ShopProfile"),
path('EditProfile/',views.EditProfile,name="EditProfile"),
path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
path("EditPhoto/", views.EditPhoto, name="EditPhoto"),

path('AddProduct/',views.AddProduct,name="AddProduct"),
path('deleteProduct/<int:did>',views.deleteProduct,name="deleteProduct"),


path('AddStock/<int:aid>/',views.AddStock,name="AddStock"),
path('deleteStock/<int:did>/<int:aid>/',views.deleteStock,name="deleteStock"),

path('Complaint/',views.Complaint,name="Complaint"),
path('DeleteComplaint/<int:did>',views.DeleteComplaint,name="DeleteComplaint"),
path('EditComplaint/<int:eid>',views.EditComplaint,name="EditComplaint"),


path('ViewBooking/',views.ViewBooking,name="ViewBooking"),
path('OrderPacked/<int:bid>',views.OrderPacked,name="OrderPacked"),
path('OrderShipped/<int:bid>/', views.OrderShipped, name='OrderShipped'),
path('OrderDelivered/<int:bid>/', views.OrderDelivered, name='OrderDelivered'),

path('ViewProductComplaint/<int:pid>/',views.ViewProductComplaint,name='ViewProductComplaint'),
path('ComplaintReply/<int:id>/',views.ComplaintReply,name="ComplaintReply"),

path('Logout/', views.Logout, name="Logout"),


path('ViewProductRating/<int:pid>/', views.ViewProductRating, name='ViewProductRating'),

path('revenue_report/',views.shop_revenue_report,name='shop_revenue_report'),

]