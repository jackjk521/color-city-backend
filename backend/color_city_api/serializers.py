from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'name', 'email', 'created']

class AnotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnotherModel
        fields = ['field1', 'field2', 'field3']

class YetAnotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = YetAnotherModel
        fields = ['fieldA', 'fieldB', 'fieldC']