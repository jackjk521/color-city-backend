from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import PurchaseHeader
from ..serializers import PurchaseHeaderSerializer

# PurchaseHeader 
class PurchaseHeaderApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the purchaseHeaders
        '''
        # category = request.query_params.get('category')

        purchaseHeaders = PurchaseHeader.objects.filter(removed = False).order_by('purchase_header_id')

        # if category:
        #     purchaseHeaders = purchaseHeaders.filter(category_id = category) 

        serializer = PurchaseHeaderSerializer(purchaseHeaders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the PurchaseHeader with given PurchaseHeader Data
        '''
        data = {
            'branch': request.data.get('branch'), # foreign key
            'user': request.data.get('user'),  # foreign key
            'transaction_type': request.data.get('transaction_type'), 
            'total_amount': request.data.get('total_amount'), 
            'payment_mode': request.data.get('payment_mode'), 
            # Add the status here if needed
        }

        serializer = PurchaseHeaderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseHeaderDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, purchase_header_id):
        '''
        Helper method to get the object with given purchase_header_id
        '''
        try:
            return PurchaseHeader.objects.get(purchase_header_id=purchase_header_id)
        except PurchaseHeader.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, purchase_header_id, *args, **kwargs):
        '''
        Retrieves the PurchaseHeader with given purchase_header_id
        '''
        purchase_header_instance = self.get_object(purchase_header_id)
        if not purchase_header_instance:
            return Response(
                {"res": "PurchaseHeader with PurchaseHeader id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PurchaseHeaderSerializer(purchase_header_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, purchase_header_id,  *args, **kwargs):
        '''
        Updates the PurchaseHeader item with given purchase_header_id if exists
        '''
        purchase_header_instance = self.get_object(purchase_header_id)
        if not purchase_header_instance:
            return Response(
                {"res": "Object with PurchaseHeader id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'branch': request.data.get('branch'), # foreign key
            'user': request.data.get('user'),  # foreign key
            'transaction_type': request.data.get('transaction_type'), 
            'total_amount': request.data.get('total_amount'), # read only and automatically updated
            'payment_mode': request.data.get('payment_mode'), 
        }

        serializer = PurchaseHeaderSerializer(instance = purchase_header_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
                purchase_header_instance.branch = serializer.validated_data['branch']
                purchase_header_instance.user = serializer.validated_data['user']
                purchase_header_instance.transaction_type = serializer.validated_data['transaction_type']
                purchase_header_instance.total_amount = serializer.validated_data['total_amount']
                purchase_header_instance.payment_mode = serializer.validated_data['payment_mode']

                # Call the update() method on the queryset to update the item
                PurchaseHeader.objects.filter(purchase_header_id=purchase_header_id).update(
                    branch=purchase_header_instance.branch,
                    user=purchase_header_instance.user,
                    transaction_type=purchase_header_instance.transaction_type,
                    total_amount= purchase_header_instance.total_amount,
                    payment_mode= purchase_header_instance.payment_mode ,                                 
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, purchase_header_id, *args, **kwargs):
        '''
        Deletes the PurchaseHeader item with given purchase_header_id if exists
        '''
        purchase_header_instance = self.get_object(purchase_header_id)
        if not purchase_header_instance:
            return Response(
                {"res": "Object with PurchaseHeader id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        purchase_header_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, purchase_header_id, *args, **kwargs):
        '''
        Soft deletes the PurchaseHeader with the given purchase_header_id if it exists
        '''
        purchase_header_instance = self.get_object(purchase_header_id)
        if not purchase_header_instance:
            return Response(
                {"res": "Object with PurchaseHeader id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        purchase_header_instance.removed = True  # Update the "removed" column to True
        purchase_header_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )
    