from rest_framework import serializers
from .models import User, Branch, Item, Category, Brand, Supplier, Inventory, PurchaseHeader, PurchaseLine

class UserSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    branch_name = serializers.CharField(source='branch.branch_name', required=False)
    # Exlcuded the password ?
    class Meta:
        model = User
        fields = ["user_id", "branch", "branch_name", "username",  "password",  "user_role", "first_name", "last_name", "age",
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
        fields = ["item_id", "item_number", "item_name", "brand", "brand_name", "category", 
                  "category_name", "unit", "package", "item_price_w_vat", "item_price_wo_vat", "retail_price", 
                  "catalyst", "created_at", "updated_at", "removed"]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "category_name", "created_at", "updated_at", "removed"]

class BrandSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    supplier_name = serializers.CharField(source='supplier.supplier_name', required=False)

    class Meta:
        model = Brand
        fields = ["brand_id", "brand_name", "supplier", "supplier_name", "created_at", "updated_at", "removed"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["supplier_id","supplier_name", "contact_num", "discount_rate", "created_at", "updated_at", "removed"]

class InventorySerializer(serializers.ModelSerializer):
    # Adding a field from another table
    item_name = serializers.CharField(source='item.item_name', required=False)
    item_price_w_vat = serializers.CharField(source='item.item_price_w_vat', required=False)
    branch_name = serializers.CharField(source='branch.branch_name', required=False)

    class Meta:
        model = Inventory
        fields = ["inventory_id", "item", "item_name", "item_price_w_vat", "branch", "branch_name", "total_quantity",
                  "holding_cost",  "created_at", "updated_at", "removed"]
        
class PurchaseHeaderSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    username = serializers.CharField(source='user.username', required=False)
    branch_name = serializers.CharField(source='branch.branch_name', required=False)
    post_status = serializers.CharField(source='purchase_header_id.post_status', required=False)
    received_status = serializers.CharField(source='purchase_header_id.received_status', required=False)
    approval_status = serializers.CharField(source='purchase_header_id.approval_status', required=False)

    class Meta:
        model = PurchaseHeader
        fields = ["purchase_header_id", "branch", "branch_name", "user", "username",  "transaction_type",
                  "total_amount", "payment_mode", "posted_status", "received_status",  "approval_status", 
                  "created_at", "updated_at", "removed"]
        
class PurchaseLineSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    item_name = serializers.CharField(source='item.item_name', required=False)
    
    class Meta:
        model = PurchaseLine
        fields = ["purchase_line_id", "purchase_header", "item", "item_name",  "req_quantity",
                  "subtotal", "status", "created_at", "updated_at", "removed"]