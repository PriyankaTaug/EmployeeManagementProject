from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from EmployeeManagementapp.models import LoginData
from EmployeeManagementapp.serializers import LoginSerializers

# Create your views here.


class LoginPage(TemplateView):
    template_name = "login.html"


class AdminLogin(View):
    def post(self,request):
        data = request.POST
        print(data)
        try:
            username = request.POST['username']
            password = request.POST['password']
            user_data = LoginData(username=username,password=password)
            if user_data is not None:
                    access_token = AccessToken.for_user(user_data)
                    refresh_token = RefreshToken.for_user(user_data)
                    return render(request,'dashboard.html',{
                        'access_token':str(access_token),
                        'refresh_token':str(refresh_token)
                    })
        except Exception as e:
            return JsonResponse({'errors': str(e)}, status=400)
