import json
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import PurchaseHeader, PurchaseLine, generate_so_number, generate_bo_number, Inventory, Item
from ..serializers import PurchaseHeaderSerializer, PurchaseLineSerializer, InventorySerializer

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

        purchaseHeaders = PurchaseHeader.objects.filter(removed = False).order_by('-purchase_header_id')

        if transaction_type:
            purchaseHeaders = purchaseHeaders.filter(transaction_type = transaction_type) 
        
        if branch_id:
            purchaseHeaders = purchaseHeaders.filter(branch_id = branch_id)
    
        if all_branches:
            purchaseHeaders = purchaseHeaders.filter(transaction_type = "BRANCH")
        
        # Exclude purchaseHeaders with status "DECLINED"
        purchaseHeaders = purchaseHeaders.exclude(status="DECLINED")
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
            return Response(purchaseHeaderSerializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Error saving purchase order data", 'errors' : purchaseHeaderSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
                {"message": "Purchase with that purchase header id does not exist"},
                status=status.HTTP_404_NOT_FOUND
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
                {"message": "Purchase order  with purchase header id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
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

            return Response(purchase_header_serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "Error updating purchase order data", 'errors' : purchase_header_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
                {"message": "Purchase order with purchase header id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        purchase_header_instance.removed = True  # Update the "removed" column to True
        purchase_header_instance.save()
        return Response(
            {"message": "Successfully removed purchase order"},
            status=status.HTTP_200_OK
        )
    
    # def soft_delete(self, request, purchase_header_id, *args, **kwargs):
    #     '''
    #     Soft deletes the PurchaseHeader with the given purchase_header_id if it exists
    #     '''
    #     purchase_header_instance = self.get_object(purchase_header_id)
    #     if not purchase_header_instance:
    #         return Response(
    #             {"message": "Object with PurchaseHeader id does not exist"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     purchase_header_instance.removed = True  # Update the "removed" column to True
    #     purchase_header_instance.save()

    #     return Response(
    #         {"message": "Object soft deleted!"},
    #         status=status.HTTP_200_OK
    #     )
# Generate PO numbers
class GenerateSONumberView(APIView):
    def get(self, request):
        so_number = generate_so_number()
        return Response(so_number)

class GenerateBONumberView(APIView):
    def get(self, request):
        bo_number = generate_bo_number()
        return Response(bo_number)
    
 # Update the status changes for purchase orders     
class UpdatePHStatusView(APIView):
   def put(self, request, purchase_header_id,  *args, **kwargs):
        try:
            purchase_header_instance = PurchaseHeader.objects.get(purchase_header_id=purchase_header_id)
        except PurchaseHeader.DoesNotExist:
            return Response(
                 {"message": "Purchase order with purchase header id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        status_value = request.data.get('status')
        purchase_lines_data = json.loads(request.data.get('purchase_lines', '[]'))

        if status_value == "POST":
            purchase_header_instance.status = "POSTED"
        elif status_value == "APPROVE":
            purchase_header_instance.status = "APPROVED"
            # Update the inventory available stock in the warehouse for each item
            for purchase_line in purchase_lines_data:
                # Get the matching inventory entry to update
                inventory_instance = Inventory.objects.get(branch= 1, item=purchase_line['item'], removed=False)
                inventory_instance.available_stock -= int(purchase_line['req_quantity'])
                inventory_instance.save()

        elif status_value == "DECLINE":
            purchase_header_instance.status = "DECLINED"
        else:
            return Response(
                {"message": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        purchase_header_instance.save()
        return Response(
            {"message": "Purchase order status updated successfully"},
            status=status.HTTP_200_OK
        )
    
# ReceiveApiView (POST - will receive multiple purchase lines and updates the received_quantity)
class ReceiveApiView(APIView):
    # Get all to be received items that have status NONE or PARTIAL
    def get(self, request, purchase_header_id, *args, **kwargs):
        
        # Check if the purchase header exists
        try:
            purchase_header_instance = PurchaseHeader.objects.get(pk=purchase_header_id)
        except PurchaseHeader.DoesNotExist:
            return Response(
                {"message": "Purchase order with purchase header id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Gets all purchase lines that have the matching purchase header and status of none or partial only
        purchase_lines = PurchaseLine.objects.filter(
            purchase_header=purchase_header_instance,
            status__in=["NONE", "PARTIAL"]
        )
        purchase_lines_serializer = PurchaseLineSerializer(purchase_lines, many=True) 

        return Response(purchase_lines_serializer.data, status=status.HTTP_200_OK)

    # Check if the received_quantity is 0 if it is then received_quantity = req_quantity otherwise update with the value given ...
    # Updates the received quantity and status of each purchase lines to COMPLETE OR PARTIAL
    # Updates the status of the purchase header to received or completed (show in the table)
    # Updates the MAIN inventory 

    # Update
    def put(self, request, purchase_header_id,  *args, **kwargs):
        # Check if the purchase header exists
        try:
            purchase_header_instance = PurchaseHeader.objects.get(pk=purchase_header_id)
        except PurchaseHeader.DoesNotExist:
            return Response(
                {"message": "Purchase order with that purchase header id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all data from the request
        complete_receive_ids = json.loads(request.data.get('completeReceive', '[]'))
        purchase_lines_data = json.loads(request.data.get('purchaseLines', '[]'))
        from_branch_id = request.data.get('from_branch')

        for purchase_line in purchase_lines_data:
            # Get the matching purchase_line to update
            line_instance = PurchaseLine.objects.get(purchase_line_id = purchase_line['purchase_line_id'])
            
            # If COMPLETE received items ALL RECEIVED the req_quantity
            if purchase_line['purchase_line_id'] in complete_receive_ids:

                # Update the fields of the purchase line object (WORKS)
                line_instance.received_quantity = purchase_line['req_quantity']
                line_instance.status =  "COMPLETED"
                line_instance.save()

                # IF item exists, update the total_quantity 
                try:
                    inventory_instance = Inventory.objects.get(branch=from_branch_id, item=purchase_line['item'], removed=False)
                    serializer = InventorySerializer(inventory_instance)

                    inventory_instance.total_quantity += int(purchase_line['req_quantity'])
                    inventory_instance.available_stock += int(purchase_line['req_quantity'])

                    inventory_instance.holding_cost = float(serializer.data['item_price_w_vat']) * float(inventory_instance.total_quantity)
                    inventory_instance.save()

                except ObjectDoesNotExist:
                    # Adds a new entry to the inventory
                    item_data = Item.objects.get(item_id=purchase_line['item'], removed=False)
                    if item_data:
                        holding_cost = float(item_data.item_price_w_vat) * int(purchase_line['req_quantity'])
                        data = {
                            'item': item_data.item_id,
                            'branch': from_branch_id,
                            'total_quantity': int(purchase_line['req_quantity']),
                            'available_stock': int(purchase_line['req_quantity']),
                            'holding_cost': holding_cost
                        }

                        serializer = InventorySerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                    # else:
                    #     # Handle the case when the item is not found
                    #     print("Item not found.")

                if int(from_branch_id) != 1: # TO BE TESTED WITH BRANCH ORDERS
                    # Deduct the received quantity from the main inventory
                    inventory_instance = Inventory.objects.get(branch=1, item=purchase_line['item'], removed=False)
                    serializer = InventorySerializer(inventory_instance)

                    inventory_instance.total_quantity -= int(purchase_line['req_quantity'])
                    inventory_instance.holding_cost = float(serializer.data['item_price_w_vat']) * float(inventory_instance.total_quantity)
                    inventory_instance.save()


            # If PARTIAL received items
            else: 

                # Update the fields of the purchase line object
                line_instance.received_quantity += int(purchase_line['receive_qty'])

                # Check if the req_quantity is equal to received_quantity
                if line_instance.req_quantity == line_instance.received_quantity:
                    line_instance.status =  "COMPLETED"
                else:
                    line_instance.status =  "PARTIAL"
                line_instance.save()

                # IF item exists, update the total_quantity 
                try:
                    inventory_instance = Inventory.objects.get(branch=from_branch_id, item=purchase_line['item'], removed=False)
                    serializer = InventorySerializer(inventory_instance)

                    inventory_instance.total_quantity += int(purchase_line['receive_qty'])
                    inventory_instance.available_stock += int(purchase_line['receive_qty'])

                    inventory_instance.holding_cost = float(serializer.data['item_price_w_vat']) * float(inventory_instance.total_quantity)
                    inventory_instance.save()

                except ObjectDoesNotExist:
                    # Adds a new entry to the inventory
                    item_data = Item.objects.get(item_id=purchase_line['item'], removed=False)
                    if item_data:
                        holding_cost = float(item_data.item_price_w_vat) * int(purchase_line['receive_qty'])
                        data = {
                            'item': item_data.item_id,
                            'branch': from_branch_id,
                            'total_quantity': int(purchase_line['receive_qty']),
                            'available_stock': int(purchase_line['receive_qty']),
                            'holding_cost': holding_cost
                        }

                        serializer = InventorySerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()

                if int(from_branch_id) != 1: # Checks if the branch is the warehouse or not
                    # Deduct the received quantity from the main inventory
                    inventory_instance = Inventory.objects.get(branch=1, item=purchase_line['item'], removed=False)
                    serializer = InventorySerializer(inventory_instance)

                    inventory_instance.total_quantity -= int(purchase_line['receive_qty'])
                    inventory_instance.holding_cost = float(serializer.data['item_price_w_vat']) * float(inventory_instance.total_quantity)
                    inventory_instance.save()

        # Update the purchase header if the number of purchase lines is equal to the purchase lines that have COMPLETED in the status
        total_purchase_lines =  PurchaseLine.objects.filter(purchase_header_id= purchase_header_id).count()
        total_completed = PurchaseLine.objects.filter(purchase_header_id= purchase_header_id, status = "COMPLETED").count()
        if(total_purchase_lines == total_completed):
            # print(total_purchase_lines == total_completed)
            purchase_header = PurchaseHeader.objects.filter(purchase_header_id=purchase_header_id)
            purchase_header.status = "COMPLETED"
            purchase_header.received_status = "COMPLETED"
            purchase_header.update(
                status = purchase_header.status,
                received_status = purchase_header.received_status
            )
            # Need to change these 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response({'message' : "Error updating purchase order data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



