from django.db import models
# from django.contrib.auth.models import User

# Helper Functions
def generate_product_number():
    return f"PN-{Item.objects.count() + 1:010d}"
# :010d (padding 10 digits max)

# Create your models here.

# User Model
class User(models.Model):
    # Fields of your model
    branch_id = models.ForeignKey("Branch", on_delete=models.DO_NOTHING,  blank = False, null = False)
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

# Branch Model
class Branch(models.Model):
    # Fields of your model
    branch_name = models.CharField(max_length = 255, blank = False, null = False)
    address = models.CharField(max_length = 255, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False, blank = True, null = True)

    class Meta:
        db_table = 'branches'

    def __str__(self):
        return self.branch_name


# Item Model
class Item(models.Model):
    # Constants
    LITERS_4 = "4L"
    LITER_1 = "L"
    PIECES = "PCS"
    GALLONS = "GL"

    PACKAGE_CHOICES = [
        (LITERS_4, "4 Liters"),
        (LITER_1, "1 Liter"),
        (PIECES, "Pieces"),
        (GALLONS, "Gallons"),
    ]

    # Fields of your model
    item_number = models.CharField(     
        max_length=20,
        default=generate_product_number,
        unique=True
    )
    item_name = models.CharField(max_length = 255, blank = False, null = False)
    total_quantity = models.IntegerField(blank = False, null = False)
    date_added = models.DateField(auto_now_add = True, auto_now = False, blank = True, null = True)
    category = models.CharField(max_length = 255, blank = True, null = True)
    unit = models.IntegerField()
    package = models.CharField(max_length = 255, choice = PACKAGE_CHOICES , default= LITERS_4 , blank = False, null = False)
    item_price_w_vat = models.DecimalField(decimal_places=2, blank = False, null = False)
    item_price_wo_vat = models.DecimalField(decimal_places=2, blank = False, null = False)
    retail_price = models.DecimalField(decimal_places=2, blank = True, null = True)
    catalyst = models.ForeignKey("Catalyst", on_delete=models.DO_NOTHING,  blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False, blank = True, null = True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.item_name

# Catalyst Model
class Catalyst(models.Model):
    # Constants
    LITER_1 = "L"
    PIECES = "PCS"

    PACKAGE_CHOICES = [
        (LITER_1, "1 Liter"),
        (PIECES, "Pieces"),
    ]

    # Fields of your model
    item_name = models.CharField(max_length = 255, blank = False, null = False)
    total_quantity = models.IntegerField(blank = False, null = False)
    unit = models.IntegerField()
    package = models.CharField(max_length = 255, choice = PACKAGE_CHOICES , default= LITERS_4 , blank = False, null = False)
    item_price_w_vat = models.DecimalField(decimal_places=2, blank = False, null = False)
    item_price_wo_vat = models.DecimalField(decimal_places=2, blank = False, null = False)
    retail_price = models.DecimalField(decimal_places=2, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True, null = True)
    removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'catalysts'

    def __str__(self):
        return self.item_name
