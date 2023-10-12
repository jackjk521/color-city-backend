from django.urls import path, include
# from .views import (
    
#     TodoListApiView,
#     TodoDetailApiView
# )

from .views.items import ItemApiView, ItemDetailApiView, GenerateItemNumberView
from .views.brands import BrandApiView, BrandDetailApiView
from .views.categories import CategoryApiView, CategoryDetailApiView


# urlpatterns = [
#     path('api', TodoListApiView.as_view()),
#     path('api/<int:todo_id>/', TodoDetailApiView.as_view()),    
# ]

urlpatterns = [
    # Items
    path('api/items', ItemApiView.as_view()),
    path('api/gen_item_number', GenerateItemNumberView.as_view()),
    path('api/item/<int:item_id>/', ItemDetailApiView.as_view()),  

    # Brands
    path('api/brands', BrandApiView.as_view()),
    path('api/brand/<int:brand_id>/', BrandDetailApiView.as_view()), 

    # Categories
    path('api/categories', CategoryApiView.as_view()),
    path('api/category/<int:category_id>/', CategoryDetailApiView.as_view()), 
]