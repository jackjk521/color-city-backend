from rest_framework import serializers
from .models import User, Branch, Item, Brand, Supplier

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

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["brand_name", "supplier_id", "created_at", "updated_at", "removed"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["supplier_name", "contact_num", "created_at", "updated_at", "removed"]
