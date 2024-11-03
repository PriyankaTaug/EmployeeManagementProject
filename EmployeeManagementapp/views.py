import hashlib
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from EmployeeManagementapp.models import *
from EmployeeManagementapp.serializers import EmployeeSerializers, LoginSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class LoginPage(TemplateView):
    template_name = "login.html"

class EmployeePage(TemplateView):
    template_name = "EmployeePage.html"

from django.contrib import messages
class AdminLogin(View):
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # First check if we have both username and password
            if not username or not password:
                messages.error(request, 'Please provide both username and password')
                return render(request, 'EmployeePage.html')
            
            # Try to get the user data
            try:
                user_data = EmployeemanagementappLogindata.objects.get(username=username, password=password, role=1)
                print("user_data",user_data)
            except EmployeemanagementappLogindata.DoesNotExist:
                messages.error(request, 'Invalid credentials')
                return render(request, 'EmployeePage.html')
            
            # If we get here, user exists and credentials are correct
            if user_data:
                # Generate tokens
                access_token = AccessToken.for_user(user_data)
                refresh_token = RefreshToken.for_user(user_data)
                
                # Get employee data
                total_employee = EmployeemanagementappEmployeeregister.objects.exclude(name='admin').count()
                employee_data = EmployeemanagementappEmployeeregister.objects.exclude(name='admin')
                
                # Return dashboard with context
                return render(request, 'dashboard.html', {
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    'total_employee': total_employee,
                    'employee_data': employee_data,
                    'username': username,
                })
            
            # If user_data is None, return to login page
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'login.html')



class EmployeeRegisteration(APIView):
    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        role = 2
        isdelete = 0
        isactive = 0
        data_result = {
            "name":name,
            "phonenumber":phonenumber,
            "email":email,
            "isdelete":isdelete,
            "isactive":isactive,
            
        }
        serializer_data = EmployeeSerializers(data=data_result)
        username = request.POST['username']
        password = request.POST['password']
        hashed_password_entered = hashlib.sha256(password.encode('utf-8')).hexdigest()
        employee_data = EmployeeRegister.objects.all()

        if serializer_data.is_valid():
            user_id = serializer_data.save()
            user_val = user_id.id
            if user_val:
                data = {
                    "user_manager": user_val,
                    "username": username,
                    "password": hashed_password_entered,
                    "role": role,
                    'employee_data': employee_data
                }
                login_data = LoginSerializers(data=data)
                if login_data.is_valid():
                    login_id = login_data.save()
                    return Response({"status":"success"})
                else:
                    user_id.delete()
                    return Response(login_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        
   
    
        
class EmployeeView(APIView):
    def get(self,request):
        employee_data = EmployeemanagementappEmployeeregister.objects.all()
        serializer_data = EmployeeSerializers(employee_data,many=True)
        return JsonResponse(serializer_data.data,safe=False)
        

        
class changePassword(APIView):
    def post(self, request):
        try:
            id =request.POST['id']
            npassword = request.POST['npassword']
            cnassword = request.POST['npassword']
            if npassword == cnassword:
                hashed_password_entered = hashlib.sha256(cnassword.encode('utf-8')).hexdigest()
                employee = EmployeemanagementappLogindata.objects.get(user_manager=id)  # Get employee by ID
                employee.password = hashed_password_entered
                employee.save()
                return Response({"status":"success"}) 
            else:
                return Response({"status":"Not matching"}) 
            
        except EmployeemanagementappEmployeeregister.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ViewProfile(APIView):
    def get(self, request):
        try:
            id = request.data.get('id')
            employee_data = EmployeeRegister.objects.get(id=id)
            return render(request,'profileview.html',{'employee_data':employee_data})
        except EmployeeRegister.DoesNotExist:
            return Response({"error": "Employee not found."},
 status=status.HTTP_404_NOT_FOUND)


# class FiledAdd(APIView):
#     def post(self,request):
#         field_name = request.POST['field_name']
#         field_type = request.POST['field_type']
#         if field_name and field_type:
#             # Example SQL command to add a column dynamically
#             sql = f'ALTER TABLE your_app_yourmodel ADD COLUMN {field_name} {field_type};'
#             with connection.cursor() as cursor:
#                 cursor.execute(sql)
            
#             return JsonResponse({'success': True, 'message': 'Column added successfully.'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid input.'})
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})

class EmployeeEdit(APIView):
    def get(self, request, id):
        employee_val = EmployeemanagementappEmployeeregister.objects.get(id=id)
        return render(request, 'employee_profile.html', {'employee_val': employee_val})
    


class EmployeeUpdate(APIView):
    def post(self, request):
        try:
            id = request.data.get('id')  # Ensure 'id' is provided in request data
            employee = EmployeemanagementappEmployeeregister.objects.get(id=id)  # Get employee by ID
            serializer = EmployeeSerializers(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeemanagementappEmployeeregister.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
class EmployeeDelete(APIView):
    def post(self, request,id):
        employee = EmployeemanagementappEmployeeregister.objects.get(id=id)  # Get employee by ID
        employee.delete()  # Delete the employee
        return Response({"status":"success"})  # Return no content status
       


class LogoutPage(APIView):
    def post(self,request):
        logout(request)
        return render(request,'login.html')
    


# Employee

from django.contrib import messages
class EmployeeLogin(View):
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            hashed_password_entered = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # First check if we have both username and password
            if not username or not password:
                messages.error(request, 'Please provide both username and password')
                return render(request, 'EmployeePage.html')
            
            # Try to get the user data
            try:
                user_data = EmployeemanagementappLogindata.objects.get(username=username, password=hashed_password_entered, role=2)
            except EmployeemanagementappLogindata.DoesNotExist:
                messages.error(request, 'Invalid credentials')
                return render(request, 'EmployeePage.html')
        
            # If we get here, user exists and credentials are correct
            if user_data:
                # Generate tokens
                employe_data =  EmployeemanagementappEmployeeregister.objects.get(id=user_data.id)
                access_token = AccessToken.for_user(user_data)
                refresh_token = RefreshToken.for_user(user_data)
                
                
                # Return dashboard with context
                return render(request, 'employeedashboard.html', {
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    'username': username,
                    'employee_val':employe_data
                })
            
            # If user_data is None, return to login page
            messages.error(request, 'Invalid credentials')
            return render(request, 'EmployeePage.html')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'EmployeePage.html')

class EmplopyeeLogoutPage(APIView):
    def post(self,request):
        logout(request)
        return render(request,'EmployeePage.html')
    

import MySQLdb

import MySQLdb

class AddNewTab(APIView):
    def post(self, request):
        try:
            conn = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='',  # Leave it empty if no password is set
                db='employeedb',
            )
        except MySQLdb.Error as e:
            return HttpResponse(f'<script>alert("Database connection error: {e}"); window.location="/viewlevel/"</script>')

        fieldname = request.POST['fieldname']
        typename = request.POST['typename']
        max_length = request.POST['max_length']
        placeholder = request.POST['placeholder']

        # Save the new column information in your model
        reg_value = EmployeemanagementappRegcolumn(
            columnname=fieldname,
            type=typename,
            placeholder=placeholder,
            fieldname=fieldname
        )
        reg_value.save()

        cursor = conn.cursor()
        try:
            if typename != "button":
                cursor.execute(f"ALTER TABLE employeemanagementapp_employeeregister ADD COLUMN {fieldname} {typename}({max_length}) NULL")
                return HttpResponse(f'<script>alert("Added column successfully."); window.location="/viewlevel/"</script>')
        except MySQLdb.OperationalError as e:
            return HttpResponse(f'<script>alert("Column already exists or error occurred: {e}"); window.location="/viewlevel/"</script>')
        finally:
            cursor.close()
            conn.close()  # Close the connection after you're done

        