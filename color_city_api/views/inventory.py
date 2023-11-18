from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Inventory
from ..serializers import InventorySerializer

# Inventory 
class InventoryApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the inventory
        '''
        branch_id = request.query_params.get('branch')

        inventory = Inventory.objects.filter(removed = False).order_by('inventory_id')

        if branch_id:
            inventory = inventory.filter(branch_id = branch_id) 

        serializer = InventorySerializer(inventory, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Inventory data can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)
        

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Inventory with given Inventory Data
        '''
        data = {
            'item': request.data.get('item'),  # foreign key
            'branch': request.data.get('branch'),  # foreign key
            'total_quantity': request.data.get('total_quantity'), 
            'available_stock': request.data.get('total_quantity'),  # for branch orders
            'holding_cost': request.data.get('holding_cost'), 
        }

        serializer = InventorySerializer(data=data)
        if serializer.is_valid():
            # Check if there is an existing entry in that inventory
            try:
                # If an entry exists, 
                inventory_instance = Inventory.objects.get(branch=data['branch'], item=data['item'], removed=False)
                serializer = InventorySerializer(inventory_instance)

                # Update the following fields: 
                # Note: Total Quantity will be treated as receive quantity
                inventory_instance.total_quantity += int(data['total_quantity'])
                inventory_instance.available_stock += int(data['total_quantity'])
                inventory_instance.holding_cost = float(serializer.data['item_price_w_vat']) * float(inventory_instance.total_quantity)
                inventory_instance.save()

            except ObjectDoesNotExist:
                # If no entry then add a new entry
                serializer.save()
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message' : "Error saving inventory data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class InventoryDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, inventory_id):
        '''
        Helper method to get the object with given inventory_id
        '''
        try:
            return Inventory.objects.get(inventory_id=inventory_id)
        except Inventory.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, inventory_id, *args, **kwargs):
        '''
        Retrieves the Inventory with given inventory_id
        '''
        inventory_instance = self.get_object(inventory_id)
        if not inventory_instance:
            return Response(
                {"message": "Inventory entry with that inventory id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InventorySerializer(inventory_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, inventory_id,  *args, **kwargs):
        '''
        Updates the Inventory item with given inventory_id if exists
        '''
        inventory_instance = self.get_object(inventory_id)
        if not inventory_instance:
            return Response(
                {"message": "Inventory entry with that inventory id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
           
        data = {
            'item': request.data.get('item'),  # foreign key
            'branch': request.data.get('branch'),  # foreign key
            'total_quantity': request.data.get('total_quantity'), 
            'available_stock': request.data.get('total_quantity'), 
            'holding_cost': request.data.get('holding_cost'), 
        }

        serializer = InventorySerializer(instance = inventory_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
            inventory_instance.item = serializer.validated_data['item']
            inventory_instance.branch = serializer.validated_data['branch']
            inventory_instance.total_quantity = serializer.validated_data['total_quantity']
            inventory_instance.available_stock = serializer.validated_data['total_quantity']
            inventory_instance.holding_cost = serializer.validated_data['holding_cost']

            inventory_instance.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'message' : "Error updating inventory data", 'errors' : serializer.errors}, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete (Soft Delete)
    def delete(self, request, inventory_id, *args, **kwargs):
        '''
        Deletes the Inventory item with given inventory_id if exists
        '''
        inventory_instance = self.get_object(inventory_id)
        if not inventory_instance:
            return Response(
                {"message": "Inventory entry with that Inventory id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Update the "removed" column to True
        inventory_instance.removed = True   
        inventory_instance.save()

        return Response(
            {"message": "Successfully removed inventory entry"},
            status=status.HTTP_200_OK
        )