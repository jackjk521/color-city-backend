from rest_framework import serializers
from .models import User, Branch, Item, Brand, Supplier

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "branch_id", "user_role", "first_name", "last_name", "age", 
                  "created_at", "updated_at", "removed"]

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["branch_id", "branch_name", "address", "created_at", "updated_at", "removed"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["item_id", "item_number", "item_name", "brand", "total_quantity", "category", 
                  "unit", "package", "item_price_w_vat", "item_price_wo_vat", "retail_price", 
                  "catalyst", "created_at", "updated_at", "removed"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["brand_id", "brand_name", "supplier_id", "created_at", "updated_at", "removed"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["supplier_id","supplier_name", "contact_num", "created_at", "updated_at", "removed"]
