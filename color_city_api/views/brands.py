from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Brand
from ..serializers import BrandSerializer

# Brand 
class BrandApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the brands
        '''
        brands = Brand.objects.filter(removed = False).order_by('brand_id')
        serializer = BrandSerializer(brands, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Brandss can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Brand with given Brand Data
        '''
        data = {
            'brand_name': request.data.get('brand_name'), 
            'supplier': request.data.get('supplier'),  # foreign key
        }

        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message' : "Error saving brand data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BrandDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, brand_id):
        '''
        Helper method to get the object with given item_id
        '''
        try:
            return Brand.objects.get(brand_id=brand_id)
        except Brand.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, brand_id, *args, **kwargs):
        '''
        Retrieves the Brand with given brand_id
        '''
        brand_instance = self.get_object(brand_id)
        if not brand_instance:
            return Response(
                {"message": "Brand with that brand id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BrandSerializer(brand_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, brand_id,  *args, **kwargs):
        '''
        Updates the Brand with given brand_id if exists
        '''
        brand_instance = self.get_object(brand_id)
        if not brand_instance:
            return Response(
                {"message": "Brand with rthat brand id does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'brand_name': request.data.get('brand_name'), 
            'supplier': request.data.get('supplier'),  
        }

        serializer = BrandSerializer(instance = brand_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the brand object
            brand_instance.brand_name = serializer.validated_data['brand_name']
            brand_instance.supplier = serializer.validated_data['supplier']
            brand_instance.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'message' : "Error updating brand data", 'errors' : serializer.errors}, status=status.HTTP_400__BAD_REQUEST)

    # 5. Delete (Soft Delete)
    def delete(self, request, brand_id, *args, **kwargs):
        '''
        Deletes the Brand with given brand_id if exists
        '''
        brand_instance = self.get_object(brand_id)
        if not brand_instance:
            return Response(
                {"message": "brand with that brand id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update the "removed" column to True
        brand_instance.removed = True  
        brand_instance.save()

        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    