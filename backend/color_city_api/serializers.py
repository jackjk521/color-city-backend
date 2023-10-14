from rest_framework import serializers
from .models import User, Branch, Item, Category, Brand, Supplier

class UserSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    branch_name = serializers.CharField(source='branch.branch_name')
    class Meta:
        model = User
        fields = ["user_id", "branch_id", "brand_name", "user_role", "first_name", "last_name", "age", 
                  "created_at", "updated_at", "removed"]

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["branch_id", "branch_name", "address", "created_at", "updated_at", "removed"]

class ItemSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    brand_name = serializers.CharField(source='brand.brand_name', required=False)
    category_name = serializers.CharField(source='category.category_name',  required=False)

    class Meta:
        model = Item
        fields = ["item_id", "item_number", "item_name", "brand", "brand_name","total_quantity", "category", 
                  "category_name", "unit", "package", "item_price_w_vat", "item_price_wo_vat", "retail_price", 
                  "catalyst", "created_at", "updated_at", "removed"]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "category_name", "created_at", "updated_at", "removed"]

class BrandSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    supplier_name = serializers.CharField(source='supplier.supplier_name')

    class Meta:
        model = Brand
        fields = ["brand_id", "brand_name", "supplier_id", "supplier_name", "created_at", "updated_at", "removed"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["supplier_id","supplier_name", "contact_num", "created_at", "updated_at", "removed"]
