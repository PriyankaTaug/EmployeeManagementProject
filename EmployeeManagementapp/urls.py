
from django.urls import path
from EmployeeManagementapp.views import AddNewTab, AdminLogin, EmplopyeeLogoutPage, EmployeeDelete, EmployeeEdit, EmployeeLogin, EmployeePage, EmployeeRegisteration, EmployeeUpdate, EmployeeView, LoginPage, LogoutPage, ViewProfile, changePassword

app_name ="EmployeeManagementapp"
urlpatterns = [
  path('',LoginPage.as_view(),name="LoginPage"),
  path('AdminLogin/',AdminLogin.as_view(),name="AdminLogin"),
  path('EmployeeRegisteration/',EmployeeRegisteration.as_view(),name="EmployeeRegisteration"),
  path('EmployeeView/',EmployeeView.as_view(),name="EmployeeView"),
  path('ViewProfile/',ViewProfile.as_view(),name="ViewProfile"),
  path('changePassword/',changePassword.as_view(),name="changePassword"),
  path('ViewProfile/',ViewProfile.as_view(),name="ViewProfile"),
  path('EmployeeEdit/<int:id>/', EmployeeEdit.as_view(), name='EmployeeEdit'),
  path('EmployeeUpdate/', EmployeeUpdate.as_view(), name='EmployeeUpdate'),
  path('EmployeeDelete/<int:id>/', EmployeeDelete.as_view(), name='EmployeeDelete'),
  path('LogoutPage/',LogoutPage.as_view(),name="LogoutPage"),
 
# Empoloyee
path('EmployeePage/',EmployeePage.as_view(),name="EmployeePage"),
path('EmployeeLogin/',EmployeeLogin.as_view(),name="EmployeeLogin"),
path('EmplopyeeLogoutPage/',EmplopyeeLogoutPage.as_view(),name="EmplopyeeLogoutPage"),
path('AddNewTab/',AddNewTab.as_view(),name="AddNewTab"),

]
