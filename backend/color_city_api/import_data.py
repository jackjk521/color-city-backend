import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'color_city_backend.settings')

from django.core.management.base import BaseCommand
from utils.import_utils import import_suppliers, import_brands

class Command(BaseCommand):
    help = "Import data from CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('model', type=str, help='Model name')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        model_name = options['model']
        
        if model_name == 'Suppliers':
            import_suppliers(csv_file)
        elif model_name == 'Brands':
            import_brands(csv_file)
        else:
            self.stdout.write(self.style.ERROR(f"Invalid model name: {model_name}"))