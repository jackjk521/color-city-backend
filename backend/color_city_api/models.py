from django.db import models, transaction
# from django.contrib.auth.models import User

# Helper Functions
def generate_product_number():
    last_item = Item.objects.order_by('-item_id').first()
    if last_item:
        last_item_number = int(last_item.item_number.split('-')[1])
        new_item_number = f"PN-{last_item_number + 1:010d}"
    else:
        new_item_number = "PN-000000001"
    return new_item_number
# :010d (padding 10 digits max)

# Create your models here.

# User Model
class User(models.Model):
    # Fields of your model
    user_id = models.BigAutoField(primary_key=True, unique=True)
    branch = models.ForeignKey("Branch", on_delete=models.DO_NOTHING,  blank = False, null = False)
    user_role = models.CharField(max_length = 100, blank = False, null = False)
    first_name = models.CharField(max_length = 255, blank = False, null = False)
    last_name = models.CharField(max_length = 255, blank = False, null = False)
    age = models.IntegerField(blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False, blank = True, null = True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user_name
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = User.objects.select_for_update().order_by('-user_id').first()
            if last_object:     
                self.user_id = last_object.user_id + 1
            else:
                self.user_id = 1
            super().save(*args, **kwargs)


# Branch Model
class Branch(models.Model):
    # Fields of your model
    branch_id = models.BigAutoField(primary_key=True, unique=True)
    branch_name = models.CharField(max_length = 255, blank = False, null = False)
    address = models.CharField(max_length = 255, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False, blank = True, null = True)

    class Meta:
        db_table = 'branches'

    def __str__(self):
        return self.branch_name
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = Branch.objects.select_for_update().order_by('-branch_id').first()
            if last_object:     
                self.branch_id = last_object.branch_id + 1
            else:
                self.branch_id = 1
            super().save(*args, **kwargs)


# Item Model
class Item(models.Model):
    # Constants
    LITER = "L"
    PIECE = "PC"
    PIECES = "PCS"
    GALLONS = "GL"

    PACKAGE_CHOICES = [
        (LITER, "Liter"),
        (PIECE, "Piece"),
        (PIECES, "Pieces"),
        (GALLONS, "Gallons"),
    ]

    # Fields of your model
    item_id =  models.BigAutoField(primary_key=True, unique=True)
    item_number = models.CharField(     
        max_length=20,
        default=generate_product_number,
        unique=True
    )
    item_name = models.CharField(max_length = 255, blank = False, null = False)
    brand = models.ForeignKey("Brand", on_delete=models.DO_NOTHING,  blank = False, null = False)
    total_quantity = models.IntegerField(blank = False, null = False)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING,  blank = False, null = False)
    unit = models.IntegerField(blank = False, null = False)
    package = models.CharField(max_length = 255, choices= PACKAGE_CHOICES , default= GALLONS , blank = False, null = False)
    item_price_w_vat = models.DecimalField(max_digits= 20, decimal_places=2, blank = False, null = False)
    item_price_wo_vat = models.DecimalField(max_digits= 20, decimal_places=2, blank = False, null = False)
    retail_price = models.DecimalField(max_digits= 20, decimal_places=2, blank = True, null = True)
    catalyst = models.IntegerField(default= 0, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False, blank = True, null = True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = Item.objects.select_for_update().order_by('-item_id').first()
            if last_object:     
                self.item_id = last_object.item_id + 1
            else:
                self.item_id = 1
            super().save(*args, **kwargs)

# Category Model
class Category(models.Model):
    # Fields of your model
    category_id = models.BigAutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length = 255, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = Category.objects.select_for_update().order_by('-category_id').first()
            if last_object:     
                self.category_id = last_object.category_id + 1
            else:
                self.category_id = 1
            super().save(*args, **kwargs)


# Brand Model
class Brand(models.Model):
    # Fields of your model
    brand_id = models.BigAutoField(primary_key=True, unique=True)
    brand_name = models.CharField(max_length = 255, blank = False, null = False)
    supplier = models.ForeignKey("Supplier", on_delete=models.DO_NOTHING,  blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.brand_name
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = Brand.objects.select_for_update().order_by('-brand_id').first()
            if last_object:     
                self.brand_id = last_object.brand_id + 1
            else:
                self.brand_id = 1
            super().save(*args, **kwargs)

# Supplier Model
class Supplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True, unique=True)
    supplier_name = models.CharField(max_length=255, blank=False, null=False)
    contact_num = models.CharField(max_length=15, blank=False, null=False)
    discount_rate = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return self.supplier_name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            last_object = Supplier.objects.select_for_update().order_by('-supplier_id').first()
            if last_object:     
                self.supplier_id = last_object.supplier_id + 1
            else:
                self.supplier_id = 1
            super().save(*args, **kwargs)