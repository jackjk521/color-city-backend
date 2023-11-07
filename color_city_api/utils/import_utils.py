import csv

def import_suppliers(csv_file_path):
    from models import Supplier
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            supplier = Supplier()
            supplier.supplier_name = row['supplier_name']
            supplier.contact_num = row['contact_num']
            supplier.discount_rate = int(row['discount_rate'])
            supplier.removed = False
            supplier.save()

def import_brands(csv_file_path):
    from models import Brand
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            brand = Brand()
            brand.brand_name = row['brand_name']
            brand.supplier_id = row['supplier_id']
            brand.removed = False
            brand.save()