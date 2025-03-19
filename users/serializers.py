from rest_framework import serializers
from .models import Customer, CafeOwner, Administrator

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CafeOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeOwner
        fields = '__all__'

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'
