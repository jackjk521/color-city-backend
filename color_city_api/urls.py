from django.urls import path, include

from .views.items import ItemApiView, ItemDetailApiView
from .views.brands import BrandApiView, BrandDetailApiView
from .views.categories import CategoryApiView, CategoryDetailApiView
from .views.users import  UserAuthApiView, UserApiView, UserDetailApiView
from .views.branches import BranchApiView, BranchDetailApiView
from .views.suppliers import SupplierApiView, SupplierDetailApiView
from .views.inventory import InventoryApiView, InventoryDetailApiView
from .views.purchaseHeaders import PurchaseHeaderApiView, PurchaseHeaderDetailApiView, GenerateBONumberView, GenerateSONumberView, ReceiveApiView, UpdatePHStatusView
from .views.purchaseLines import PurchaseLineApiView, PurchaseLineDetailApiView
from .views.logs import LogApiView, LogDetailApiView

# urlpatterns = [
#     path('api', TodoListApiView.as_view()),
#     path('api/<int:todo_id>/', TodoDetailApiView.as_view()),    
# ]

urlpatterns = [
     # Users
    path('api/users', UserApiView.as_view()),
    path('api/auth_user/',  UserAuthApiView.as_view()),
    path('api/user/<int:user_id>/', UserDetailApiView.as_view()),  

     # Branches
    path('api/branches', BranchApiView.as_view()),
    path('api/branch/<int:branch_id>/', BranchDetailApiView.as_view()),  

     # Suppliers
    path('api/suppliers', SupplierApiView.as_view()),
    path('api/supplier/<int:supplier_id>/', SupplierDetailApiView.as_view()),  

    # Items
    path('api/items/', ItemApiView.as_view()),
    # path('api/gen_item_number', GenerateItemNumberView.as_view()),
    path('api/item/<int:item_id>/', ItemDetailApiView.as_view()),  

    # Brands
    path('api/brands', BrandApiView.as_view()),
    path('api/brand/<int:brand_id>/', BrandDetailApiView.as_view()), 

    # Categories
    path('api/categories', CategoryApiView.as_view()),
    path('api/category/<int:category_id>/', CategoryDetailApiView.as_view()), 

    # Inventory
    path('api/inventory/', InventoryApiView.as_view()),
    path('api/inv/<int:inventory_id>/', InventoryDetailApiView.as_view()),  
    
    # Supplier and Branch Orders: Purchase Headers and Purchase Lines
    path('api/purchases/', PurchaseHeaderApiView.as_view()),
    path('api/gen_so_number', GenerateSONumberView.as_view()),
    path('api/gen_bo_number', GenerateBONumberView.as_view()),
    path('api/receiving/<int:purchase_header_id>/', ReceiveApiView.as_view()),
    path('api/po_status/<int:purchase_header_id>/', UpdatePHStatusView.as_view()),
    path('api/purchases/', PurchaseHeaderApiView.as_view()),
    path('api/purchases/<int:purchase_header_id>/', PurchaseHeaderDetailApiView.as_view()),  

    # # Purchase Lines
    path('api/purchase_lines', PurchaseLineApiView.as_view()),
    path('api/purchase_line/<int:purchase_line_id>/', PurchaseLineDetailApiView.as_view()),

    # Logs
    path('api/logs', LogApiView.as_view()),  
]