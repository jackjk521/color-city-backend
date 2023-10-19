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
        # category = request.query_params.get('category')

        inventory = Inventory.objects.filter(removed = False).order_by('inventory_id')

        # if category:
        #     inventory = inventory.filter(category_id = category) 

        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Inventory with given Inventory Data
        '''
        data = {
            'item': request.data.get('item'),  # foreign key
            'branch': request.data.get('branch'),  # foreign key
            'total_quantity': request.data.get('total_quantity'), 
            'holding_cost': request.data.get('holding_cost'), 
        }

        serializer = InventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                {"res": "Inventory with Inventory id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
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
                {"res": "Object with Inventory id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'item': request.data.get('item'),  # foreign key
            'branch': request.data.get('branch'),  # foreign key
            'total_quantity': request.data.get('total_quantity'), 
            'holding_cost': request.data.get('holding_cost'), 
        }

        serializer = InventorySerializer(instance = inventory_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
                inventory_instance.item = serializer.validated_data['item']
                inventory_instance.branch = serializer.validated_data['branch']
                inventory_instance.total_quantity = serializer.validated_data['total_quantity']
                inventory_instance.holding_cost = serializer.validated_data['holding_cost']

                # Call the update() method on the queryset to update the item
                Inventory.objects.filter(inventory_id=inventory_id).update(
                    item=inventory_instance.item,
                    branch=inventory_instance.branch,
                    total_quantity=inventory_instance.total_quantity,
                    holding_cost= inventory_instance.holding_cost,
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, inventory_id, *args, **kwargs):
        '''
        Deletes the Inventory item with given inventory_id if exists
        '''
        inventory_instance = self.get_object(inventory_id)
        if not inventory_instance:
            return Response(
                {"res": "Object with Inventory id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        inventory_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, inventory_id, *args, **kwargs):
        '''
        Soft deletes the Inventory with the given inventory_id if it exists
        '''
        inventory_instance = self.get_object(inventory_id)
        if not inventory_instance:
            return Response(
                {"res": "Object with Inventory id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        inventory_instance.removed = True  # Update the "removed" column to True
        inventory_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )
    