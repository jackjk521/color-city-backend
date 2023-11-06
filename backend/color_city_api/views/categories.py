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
        categories = Category.objects.filter(removed = False).order_by('category_id')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Category with given Category Data
        '''
        data = {
            'category_name': request.data.get('category_name'), 
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
    def put(self, request, category_id,  *args, **kwargs):
        '''
        Updates the Category with given category_id if exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with Category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'category_name': request.data.get('category_name'), 
        }

        serializer = CategorySerializer(instance = category_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the brand object
            category_instance.category_name = serializer.validated_data['category_name']
            category_instance.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)

    # 5. Delete
    def delete(self, request, category_id, *args, **kwargs):
        '''
        Deletes the Category with given category_id if exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with Category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # Update the "removed" column to True
        category_instance.removed = True  
        category_instance.save()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )