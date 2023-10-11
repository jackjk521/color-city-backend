from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Category
from ..serializers import CategorySerializer

# Category 
class CategoryApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the categories
        '''
        categories = Category.objects.filter(removed = False)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create 
    def post(self, request, *args, **kwargs):
        '''
        Create the Category with given Category Data
        '''
        data = {
            'item_name': request.data.get('item_name'), 
            'brand': request.data.get('brand'),  # foreign key
            'total_quantity': request.data.get('total_quantity'), 
            'category': request.data.get('category'), # foreign key
            'unit': request.data.get('unit'), 
            'package': request.data.get('package'), 
            'item_price_w_vat': request.data.get('item_price_w_vat'), 
            'item_price_wo_vat': request.data.get('item_price_wo_vat'), 
            'retail_price': request.data.get('retail_price'), 
            'catalyst': request.data.get('catalyst'), # not a foreign key but will hold the item_id of the catalyst
        }

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, category_id):
        '''
        Helper method to get the object with given category_id
        '''
        try:
            return Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, category_id, *args, **kwargs):
        '''
        Retrieves the Category with given category_id
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Category with Category id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CategorySerializer(category_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, category_id, *args, **kwargs):
        '''
        Updates the Category category with given category_id if exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with Category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'item_name': request.data.get('item_name'), 
            'brand': request.data.get('brand'), 
            'total_quantity': request.data.get('total_quantity'), 
            'category': request.data.get('category'), 
            'unit': request.data.get('unit'), 
            'package': request.data.get('package'), 
            'item_price_w_vat': request.data.get('item_price_w_vat'), 
            'item_price_wo_vat': request.data.get('item_price_wo_vat'), 
            'retail_price': request.data.get('retail_price'), 
            'catalyst': request.data.get('catalyst'), 
        }
        serializer = CategorySerializer(instance = item_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, item_id, *args, **kwargs):
        '''
        Deletes the Category item with given item_id if exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Object with Category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        item_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, item_id, *args, **kwargs):
        '''
        Soft deletes the Category with the given item_id if it exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Object with Category id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item_instance.removed = True  # Update the "removed" column to True
        item_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )