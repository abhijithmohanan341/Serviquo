from django.urls import path,include
from Basics import views 
urlpatterns = [
  path('sum/',views.sum),
  path('calculator',views.calculator),  

]