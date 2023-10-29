import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import PurchaseHeader, PurchaseLine, generate_so_number, generate_bo_number
from ..serializers import PurchaseHeaderSerializer, PurchaseLineSerializer

# PurchaseHeader + Purchase Lines
class PurchaseHeaderApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the purchaseHeaders
        '''
        transaction_type = request.query_params.get('type')
        all_branches = request.query_params.get('all_branches')
        branch_id = request.query_params.get('branch')

        purchaseHeaders = PurchaseHeader.objects.filter(removed = False).order_by('purchase_header_id')

        if transaction_type:
            purchaseHeaders = purchaseHeaders.filter(transaction_type = transaction_type) 
        
        if branch_id:
            purchaseHeaders = purchaseHeaders.filter(branch_id = branch_id) 
                    
        if all_branches:
            purchaseHeaders = purchaseHeaders.filter(transaction_type = "BRANCH") 

        purchase_header_serializer = PurchaseHeaderSerializer(purchaseHeaders, many=True)
        response_data = []
        for purchase_header in purchase_header_serializer.data:
            # Get all matching purchase lines 
            purchase_lines = PurchaseLine.objects.filter(purchase_header_id=purchase_header['purchase_header_id'])
            purchase_lines_serializer = PurchaseLineSerializer(purchase_lines, many=True)
            # Add the purchase lines to each purchase header entry 
            purchase_header['purchase_lines'] = purchase_lines_serializer.data
            response_data.append(purchase_header)

        return Response(response_data, status=status.HTTP_200_OK)  

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the PurchaseHeader with given PurchaseHeader Data
        '''

        data = {
            'branch': request.data.get('purchaseHeader[branch]'),
            'user': request.data.get('purchaseHeader[user]'),
            'supplier': request.data.get('purchaseHeader[supplier]'),
            'po_number': request.data.get('purchaseHeader[po_number]'),
            'transaction_type': request.data.get('purchaseHeader[transaction_type]'),
            'total_amount': request.data.get('purchaseHeader[total_amount]'),
            'payment_mode': request.data.get('purchaseHeader[payment_mode]'),
            'status': request.data.get('purchaseHeader[status]'),
            # Add the status here if needed
        }

        purchaseHeaderSerializer = PurchaseHeaderSerializer(data=data)

        # Add the insertion of purchase lines 
        if purchaseHeaderSerializer.is_valid():
            purchase_header = purchaseHeaderSerializer.save()

             # Insert purchase lines
            purchase_lines = json.loads(request.data.get('purchaseLines', '[]'))
            for purchase_line_data in purchase_lines:
                purchase_line_data['purchase_header'] = purchase_header.purchase_header_id
                purchaseLineSerializer = PurchaseLineSerializer(data=purchase_line_data)
                if purchaseLineSerializer.is_valid():
                    purchaseLineSerializer.save()
                else:
                    # Handle invalid purchase line data
                     # Handle invalid purchase line data
                    print(purchaseLineSerializer.errors)  # Print the validation errors for debugging purposes
                    return Response(purchaseLineSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(purchaseHeaderSerializer.data, status=status.HTTP_201_CREATED)

        return Response(purchaseHeaderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        purchase_header_serializer = PurchaseHeaderSerializer(purchase_header_instance)
        purchase_lines = PurchaseLine.objects.filter(purchase_header_id=purchase_header_instance.purchase_header_id)
        purchase_lines_serializer = PurchaseLineSerializer(purchase_lines, many=True)

        response_data = {
            "purchase_header": purchase_header_serializer.data,
            "purchase_lines": purchase_lines_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

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
            'branch': request.data.get('purchaseHeader[branch]'),
            'user': request.data.get('purchaseHeader[user]'),
            'supplier': request.data.get('purchaseHeader[supplier]'),
            'transaction_type': request.data.get('purchaseHeader[transaction_type]'),
            'total_amount': request.data.get('purchaseHeader[total_amount]'),
            'payment_mode': request.data.get('purchaseHeader[payment_mode]'),
            'status': request.data.get('purchaseHeader[status]'),
            # Add the status here if needed
        }

        purchase_header_serializer = PurchaseHeaderSerializer(instance = purchase_header_instance, data=data, partial = True)

        if purchase_header_serializer.is_valid():
            purchase_header = purchase_header_serializer.save()

            # Update purchase lines
            purchase_lines = json.loads(request.data.get('purchaseLines', '[]'))

            # Delete existing purchase lines related to the purchase header
            PurchaseLine.objects.filter(purchase_header_id= purchase_header.purchase_header_id).delete()

            for purchase_line in purchase_lines:
                # Access individual properties of each purchase_line object
                purchase_line['purchase_header'] = purchase_header.purchase_header_id
                purchaseLineSerializer = PurchaseLineSerializer(data=purchase_line)

                if purchaseLineSerializer.is_valid():
                    purchaseLineSerializer.save()
                else:
                    # Handle invalid purchase line data
                    # You may choose to raise an exception, return a specific response, etc.
                    return Response(purchaseLineSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(purchase_header_serializer.data, status=status.HTTP_200_OK)

        return Response(purchase_header_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if purchase_header_serializer.is_valid():
        #     # Update the fields of the item object
        #         purchase_header_instance.branch = purchase_header_serializer.validated_data['branch']
        #         purchase_header_instance.user = purchase_header_serializer.validated_data['user']
        #         purchase_header_instance.transaction_type = purchase_header_serializer.validated_data['transaction_type']
        #         purchase_header_instance.total_amount = purchase_header_serializer.validated_data['total_amount']
        #         purchase_header_instance.payment_mode = purchase_header_serializer.validated_data['payment_mode']

        #         # Call the update() method on the queryset to update the item
        #         PurchaseHeader.objects.filter(purchase_header_id=purchase_header_id).update(
        #             branch=purchase_header_instance.branch,
        #             user=purchase_header_instance.user,
        #             transaction_type=purchase_header_instance.transaction_type,
        #             total_amount= purchase_header_instance.total_amount,
        #             payment_mode= purchase_header_instance.payment_mode ,                                 
        #             # Update other fields as needed
        #         )

        #         return Response(purchase_header_serializer.data)
        # return Response(purchase_header_serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
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

class GenerateSONumberView(APIView):
    def get(self, request):
        so_number = generate_so_number()
        return Response(so_number)

class GenerateBONumberView(APIView):
    def get(self, request):
        bo_number = generate_bo_number()
        return Response(bo_number)