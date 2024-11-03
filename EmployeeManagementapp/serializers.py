from rest_framework import serializers

from EmployeeManagementapp.models import *

class LoginSerializers(serializers.Serializer):
    class Meta:
        model = EmployeemanagementappLogindata
        fields = "__all__"


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model= EmployeemanagementappEmployeeregister
        fields='__all__'
        
