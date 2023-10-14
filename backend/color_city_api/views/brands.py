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
        return Response(serializer.data, status=status.HTTP_200_OK)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                {"res": "Brand with Brand id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
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
                {"res": "Object with Item id does not exists"}, 
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

                # Call the update() method on the queryset to update the item
                Brand.objects.filter(brand_id=brand_id).update(
                    brand_name=brand_instance.brand_name,
                    supplier=brand_instance.supplier,
                
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)

    # 5. Delete
    def delete(self, request, brand_id, *args, **kwargs):
        '''
        Deletes the Brand with given brand_id if exists
        '''
        brand_instance = self.get_object(brand_id)
        if not brand_instance:
            return Response(
                {"res": "Object with Brand id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        brand_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, brand_id, *args, **kwargs):
        '''
        Soft deletes the Brand with the given brand_id if it exists
        '''
        brand_instance = self.get_object(brand_id)
        if not brand_instance:
            return Response(
                {"res": "Object with Brand id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        brand_instance.removed = True  # Update the "removed" column to True
        brand_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )