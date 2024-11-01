from rest_framework import serializers

from EmployeeManagementapp.models import LoginData

class LoginSerializers(serializers.Serializer):
    class Meta:
        model = LoginData
        fields = "__all__"