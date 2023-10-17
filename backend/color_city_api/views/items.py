from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Item, generate_product_number
from ..serializers import ItemSerializer
from django.shortcuts import get_object_or_404

# Item 
class ItemApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the items
        '''
        category = request.query_params.get('category')

        items = Item.objects.filter(removed = False).order_by('item_id')

        if category:
            items = items.filter(category_id = category) 

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Item with given Item Data
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

        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, item_id):
        '''
        Helper method to get the object with given item_id
        '''
        try:
            return Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, item_id, *args, **kwargs):
        '''
        Retrieves the Item with given item_id
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Item with Item id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ItemSerializer(item_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, item_id,  *args, **kwargs):
        '''
        Updates the Item item with given item_id if exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Object with Item id does not exists"}, 
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

        serializer = ItemSerializer(instance = item_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
                item_instance.item_name = serializer.validated_data['item_name']
                item_instance.brand = serializer.validated_data['brand']
                item_instance.total_quantity = serializer.validated_data['total_quantity']
                item_instance.category = serializer.validated_data['category']
                item_instance.unit = serializer.validated_data['unit']
                item_instance.package = serializer.validated_data['package']
                item_instance.item_price_w_vat = serializer.validated_data['item_price_w_vat']
                item_instance.item_price_wo_vat = serializer.validated_data['item_price_wo_vat']
                item_instance.retail_price = serializer.validated_data['retail_price']
                item_instance.catalyst = serializer.validated_data['catalyst']

                # Call the update() method on the queryset to update the item
                Item.objects.filter(item_id=item_id).update(
                    item_name=item_instance.item_name,
                    brand=item_instance.brand,
                    total_quantity=item_instance.total_quantity,
                    category= item_instance.category,
                    unit= item_instance.unit  ,                                 
                    item_price_w_vat = item_instance.item_price_w_vat,
                    item_price_wo_vat = item_instance.item_price_wo_vat ,
                    retail_price = item_instance.retail_price,
                    catalyst = item_instance.catalyst,
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, item_id, *args, **kwargs):
        '''
        Deletes the Item item with given item_id if exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Object with Item id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        item_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, item_id, *args, **kwargs):
        '''
        Soft deletes the Item with the given item_id if it exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"res": "Object with Item id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item_instance.removed = True  # Update the "removed" column to True
        item_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )
    
class GenerateItemNumberView(APIView):
    def get(self, request):
        item_number = generate_product_number()
        return Response(item_number)