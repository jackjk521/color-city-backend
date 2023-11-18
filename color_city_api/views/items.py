from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Item, Log
from ..serializers import ItemSerializer, LogSerializer
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
        if serializer: 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Items can not be retrieved", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Item with given Item Data
        '''

        data = {
            'item_id': request.data.get('item_id'), 
            'item_number': request.data.get('item_number'), 
            'item_name': request.data.get('item_name'), 
            'brand': request.data.get('brand'),  # foreign key
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

        return Response({"message": "Error saving the item data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
                {"message": "Item with that ttem id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # brand_item = request.query_params.get('item_name')

        # if brand_item:
        #     serializer = ItemSerializer(item_instance)
        #     brand_item_formatted = f"{serializer.data['brand_name']} - {serializer.data['item_name']}"
        #     return Response(brand_item_formatted, status=status.HTTP_200_OK)
        # else: 
        #     serializer = ItemSerializer(item_instance)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, item_id,  *args, **kwargs):
        '''
        Updates the Item item with given item_id if exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"message": "Item with that ttem id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
           
        data = {
            'item_number': request.data.get('item_number'), 
            'item_name': request.data.get('item_name'), 
            'brand': request.data.get('brand'), 
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
            item_instance.item_number = serializer.validated_data['item_number']
            item_instance.item_name = serializer.validated_data['item_name']
            item_instance.brand = serializer.validated_data['brand']
            item_instance.category = serializer.validated_data['category']
            item_instance.unit = serializer.validated_data['unit']
            item_instance.package = serializer.validated_data['package']
            item_instance.item_price_w_vat = serializer.validated_data['item_price_w_vat']
            item_instance.item_price_wo_vat = serializer.validated_data['item_price_wo_vat']
            item_instance.retail_price = serializer.validated_data['retail_price']
            item_instance.catalyst = serializer.validated_data['catalyst']
            item_instance.save()

            # user_data = request.session.get('user_data')

            # if user_data is None:
            #     return Response({'message': 'User data not found in session'}, status=status.HTTP_400_BAD_REQUEST)

            # log_data = {
            #     'branch': user_data['branch'],
            #     'user': user_data['user_id'],
            #     'type': "ITEMS",
            #     'type_id': request.data.get('item_id'),
            #     'message': f"{user_data['username']} successfully updated item with item_id {request.data.get('item_id')}."
            # }
            # logSerializer = LogSerializer(data=log_data)

            # if logSerializer.is_valid():
            #     logSerializer.save()

            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response({'message' : "Error updating item data", 'errors' : serializer.errors}, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, item_id, *args, **kwargs):
        '''
        Deletes the Item item with given item_id if exists
        '''
        item_instance = self.get_object(item_id)
        if not item_instance:
            return Response(
                {"message": "Item with that item id does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # Update the "removed" column to True
        item_instance.removed = True  
        item_instance.save()
        return Response(
            {"message": "Successfully removed item"},
            status=status.HTTP_200_OK
        )
