from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Supplier
from ..serializers import SupplierSerializer
from django.shortcuts import get_object_or_404

# Supplier 
class SupplierApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the suppliers
        '''
        suppliers = Supplier.objects.filter(removed = False).order_by('supplier_id')
        serializer = SupplierSerializer(suppliers, many=True)
        if serializer:   
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Suppliers can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)


    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Supplier with given Supplier Data
        '''
        data = {
            'supplier_name': request.data.get('supplier_name'), 
            'contact_num': request.data.get('contact_num'),
            'discount_rate': request.data.get('discount_rate'), 
        }

        serializer = SupplierSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message' : "Error saving supplier data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SupplierDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, supplier_id):
        '''
        Helper method to get the object with given supplier_id
        '''
        try:
            return Supplier.objects.get(supplier_id=supplier_id)
        except Supplier.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, supplier_id, *args, **kwargs):
        '''
        Retrieves the Supplier with given supplier_id
        '''
        supplier_instance = self.get_object(supplier_id)
        if not supplier_instance:
            return Response(
                {"message": "Supplier with that supplier id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SupplierSerializer(supplier_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, supplier_id,  *args, **kwargs):
        '''
        Updates the Supplier item with given supplier_id if exists
        '''
        supplier_instance = self.get_object(supplier_id)
        if not supplier_instance:
            return Response(
                {"message": "Supplier with that supplier id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
           
        data = {
            'supplier_name': request.data.get('supplier_name'), 
            'contact_num': request.data.get('contact_num'),
            'discount_rate': request.data.get('discount_rate'), 
        }

        serializer = SupplierSerializer(instance = supplier_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
            supplier_instance.supplier_name = serializer.validated_data['supplier_name']
            supplier_instance.contact_num = serializer.validated_data['contact_num']
            supplier_instance.discount_rate = serializer.validated_data['discount_rate']
            supplier_instance.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Error updating supplier data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                        
    # 5. Delete (Soft Delete)
    def delete(self, request, supplier_id, *args, **kwargs):
        '''
        Deletes the Supplier item with given supplier_id if exists
        '''
        supplier_instance = self.get_object(supplier_id)
        if not supplier_instance:
            return Response(
                {"message": "Supplier with that supplier id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Update the "removed" column to True
        supplier_instance.removed = True  
        supplier_instance.save()
        return Response(
            {"message": "Successfully removed supplier"},
            status=status.HTTP_200_OK
        )