from rest_framework import serializers
from .models import User, Branch, Item, Catalyst 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["branch_id", "user_role", "first_name", "last_name", "age", 
                  "created_at", "updated_at", "removed"]

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["branch_name", "address", "created_at", "updated_at", "removed"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["item_number", "item_name", "total_quantity", "date_added", "category", 
                  "unit", "package", "item_quantity_w_vat", "item_quantity_wo_vat", "retail_price", 
                  "catalyst", "created_at", "updated_at", "removed"]

class CatalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalyst
        fields = ["item_name", "total_quantity", "unit", "package", "item_quantity_w_vat", 
                  "item_quantity_wo_vat", "retail_price", "created_at", "updated_at", "removed"]

