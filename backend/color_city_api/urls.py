from django.urls import path, include
# from .views import (
    
#     TodoListApiView,
#     TodoDetailApiView
# )

from .views.items import ItemApiView, ItemDetailApiView

# urlpatterns = [
#     path('api', TodoListApiView.as_view()),
#     path('api/<int:todo_id>/', TodoDetailApiView.as_view()),    
# ]

urlpatterns = [
    # Items
    path('api/items', ItemApiView.as_view()),
    path('api/item/<int:item_id>/', ItemDetailApiView.as_view()),    
]