from django.urls import path, include

from .views.items import ItemApiView, ItemDetailApiView, GenerateItemNumberView
from .views.brands import BrandApiView, BrandDetailApiView
from .views.categories import CategoryApiView, CategoryDetailApiView
from .views.users import UserApiView, UserDetailApiView
from .views.branches import BranchApiView, BranchDetailApiView
from .views.suppliers import SupplierApiView, SupplierDetailApiView



# urlpatterns = [
#     path('api', TodoListApiView.as_view()),
#     path('api/<int:todo_id>/', TodoDetailApiView.as_view()),    
# ]

urlpatterns = [
     # Users
    path('api/users', UserApiView.as_view()),
    path('api/user/<int:user_id>/', UserDetailApiView.as_view()),  

     # Branches
    path('api/branches', BranchApiView.as_view()),
    path('api/branch/<int:branch_id>/', BranchDetailApiView.as_view()),  

     # Suppliers
    path('api/suppliers', SupplierApiView.as_view()),
    path('api/supplier/<int:supplier_id>/', SupplierDetailApiView.as_view()),  

    # Items
    path('api/items/', ItemApiView.as_view()),
    path('api/gen_item_number', GenerateItemNumberView.as_view()),
    path('api/item/<int:item_id>/', ItemDetailApiView.as_view()),  

    # Brands
    path('api/brands', BrandApiView.as_view()),
    path('api/brand/<int:brand_id>/', BrandDetailApiView.as_view()), 

    # Categories
    path('api/categories', CategoryApiView.as_view()),
    path('api/category/<int:category_id>/', CategoryDetailApiView.as_view()), 
]