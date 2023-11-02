from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import PurchaseLine
from ..serializers import PurchaseLineSerializer

# PurchaseLine 
class PurchaseLineApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the purchaseLines
        '''
        # category = request.query_params.get('category')

        purchaseLines = PurchaseLine.objects.filter(removed = False).order_by('purchase_line_id')

        # if category:
        #     purchaseLines = purchaseLines.filter(category_id = category) 

        serializer = PurchaseLineSerializer(purchaseLines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the PurchaseLine with given PurchaseLine Data
        '''
        data = {
            'purchase_header': request.data.get('purchase_header'), # foreign key
            'item': request.data.get('item'),  # foreign key
            'req_quantity': request.data.get('req_quantity'), 
            'subtotal': request.data.get('subtotal'), 
            'status': request.data.get('status'), 
            # Add the status here if needed
        }

        serializer = PurchaseLineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseLineDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, purchase_line_id):
        '''
        Helper method to get the object with given purchase_line_id
        '''
        try:
            return PurchaseLine.objects.get(purchase_line_id=purchase_line_id)
        except PurchaseLine.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, purchase_line_id, *args, **kwargs):
        '''
        Retrieves the PurchaseLine with given purchase_line_id
        '''
        purchase_line_instance = self.get_object(purchase_line_id)
        if not purchase_line_instance:
            return Response(
                {"res": "PurchaseLine with PurchaseLine id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PurchaseLineSerializer(purchase_line_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, purchase_line_id,  *args, **kwargs):
        '''
        Updates the PurchaseLine item with given purchase_line_id if exists
        '''
        purchase_line_instance = self.get_object(purchase_line_id)
        if not purchase_line_instance:
            return Response(
                {"res": "Object with PurchaseLine id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'purchase_header': request.data.get('purchase_header'), # foreign key
            'item': request.data.get('item'),  # foreign key
            'req_quantity': request.data.get('req_quantity'), 
            'subtotal': request.data.get('subtotal'), 
            'status': request.data.get('status'), 
        }

        serializer = PurchaseLineSerializer(instance = purchase_line_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
                purchase_line_instance.purchase_header = serializer.validated_data['purchase_header']
                purchase_line_instance.item = serializer.validated_data['item']
                purchase_line_instance.req_quantity = serializer.validated_data['req_quantity']
                purchase_line_instance.subtotal = serializer.validated_data['subtotal']
                purchase_line_instance.status = serializer.validated_data['payment_mode']

                # Call the update() method on the queryset to update the item
                PurchaseLine.objects.filter(purchase_line_id=purchase_line_id).update(
                    purchase_header=purchase_line_instance.purchase_header,
                    item=purchase_line_instance.item,
                    req_quantity=purchase_line_instance.req_quantity,
                    subtotal= purchase_line_instance.subtotal,
                    status= purchase_line_instance.status ,                                 
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, purchase_line_id, *args, **kwargs):
        '''
        Deletes the PurchaseLine item with given purchase_line_id if exists
        '''
        purchase_line_instance = self.get_object(purchase_line_id)
        if not purchase_line_instance:
            return Response(
                {"res": "Object with PurchaseLine id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        purchase_line_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, purchase_line_id, *args, **kwargs):
        '''
        Soft deletes the PurchaseLine with the given purchase_line_id if it exists
        '''
        purchase_line_instance = self.get_object(purchase_line_id)
        if not purchase_line_instance:
            return Response(
                {"res": "Object with PurchaseLine id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        purchase_line_instance.removed = True  # Update the "removed" column to True
        purchase_line_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )
    