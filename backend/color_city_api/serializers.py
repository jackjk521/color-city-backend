from rest_framework import serializers
from .models import User, Branch, Item, Category, Brand, Supplier, Inventory, PurchaseHeader, PurchaseLine, Log

class UserSerializer(serializers.ModelSerializer):
    # # Adding a field from another table
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
        fields = ["item_id", "item_number", "item_name", "brand_item", "brand", "brand_name", "category", 
                "category_name", "unit", "package", "item_price_w_vat", "item_price_wo_vat", "retail_price", 
                "catalyst", "created_at", "updated_at", "removed"]
        
        read_only_fields = ["brand_item"]

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
    supplier_name = serializers.CharField(source='supplier.supplier_name', required=False)

    class Meta:
        model = PurchaseHeader
        fields = ["purchase_header_id", "branch", "branch_name", "user", "username",  "transaction_type", "po_number", "supplier",
                "supplier_name", "total_amount", "payment_mode", "status", "date_created", "status",  "received_status", 
                "created_at", "updated_at", "removed"]
        # Set the required attribute of supplier field to False
        extra_kwargs = {
            'supplier': {'required': False}
        }
        
class PurchaseLineSerializer(serializers.ModelSerializer):
    # Adding a field from another table
    item_name = serializers.CharField(source='item.item_name', required=False)
    # item_price_w_vat = serializers.CharField(source='item.item_price_w_vat', required=False)
    brand_item = serializers.CharField(source='item.brand_item', read_only=True, required=False)

    # If i remove item_price_w_vat  it works
    class Meta:
        model = PurchaseLine
        fields = ["purchase_line_id", "purchase_header", "item", "item_name", "brand_item",  "req_quantity",
                "subtotal", "status", "created_at", "updated_at", "removed"]

    # def create(self, validated_data):
    #         purchase_line = PurchaseLine()
    #         purchase_line.purchase_header = validated_data.get('purchase_header')
    #         purchase_line.item = validated_data.get('item')
    #         purchase_line.req_quantity = validated_data.get('req_quantity')
    #         purchase_line.subtotal = validated_data.get('subtotal') 
            
    #         purchase_line.save()
    #         return purchase_line
        
class LogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Log
        fields = ["log_id", "branch", "user", "type",  "type_id", "message",
                "created_at", "updated_at", "removed"]