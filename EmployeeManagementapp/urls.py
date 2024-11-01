
from django.urls import path
from EmployeeManagementapp.views import AdminLogin, LoginPage

app_name ="EmployeeManagementapp"
urlpatterns = [
  path('',LoginPage.as_view(),name="LoginPage"),
  path('AdminLogin/',AdminLogin.as_view(),name="AdminLogin")
]
