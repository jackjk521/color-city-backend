from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from ..models import User, Item, Inventory, PurchaseHeader, Branch
from ..serializers import UserSerializer, PurchaseHeaderSerializer, InventorySerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, Extract

# Today date and Weekly date range
today = timezone.now().date()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=5)
current_year = timezone.now().date().year


# Dashboard Data
class DashboardApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the dashboard data
        '''
        _type = request.query_params.get('type')
        if(_type == "summary"):
            # Count of Users / Employees
            users = User.objects.filter(removed = False).count()
            
            # Count of Branches
            branches = Branch.objects.filter(removed = False).count()

            # Count of Items
            items = Item.objects.filter(removed = False).count()

            response_data = {
            "users": users,
            "branches": branches,
            "items": items,
        }

        if(_type == "orders_overview"):

            # Get the total number of for approval orders
            for_approval_total = PurchaseHeader.objects.filter(status = "POSTED", removed = False, created_at__date__range=[start_of_week, end_of_week]).count()
             # Get the total number of for approval orders
            pending_total = PurchaseHeader.objects.filter(status = "APPROVED", removed = False, created_at__date__range=[start_of_week, end_of_week]).count()
             # Get the total number of for approval orders
            completed_total = PurchaseHeader.objects.filter(status = "COMPLETED", removed = False, created_at__date__range=[start_of_week, end_of_week]).count()

            
            # Get all for approval orders
            for_approval_orders = PurchaseHeader.objects.filter(status = "POSTED", removed = False, created_at__date__range=[start_of_week, end_of_week]).order_by("-purchase_header_id")
            # Get all to be received orders
            pending_orders = PurchaseHeader.objects.filter(status = "APPROVED", removed = False, created_at__date__range=[start_of_week, end_of_week]).order_by("-purchase_header_id")
            # Get all completed orders
            completed_orders = PurchaseHeader.objects.filter(status = "COMPLETED", removed = False, created_at__date__range=[start_of_week, end_of_week]).order_by("-purchase_header_id")

            # Return orders data
            for_approval_orders_data = PurchaseHeaderSerializer(for_approval_orders, many=True)
            pending_orders_data = PurchaseHeaderSerializer(pending_orders, many=True)
            completed_orders_data = PurchaseHeaderSerializer(completed_orders, many=True)

            response_data = {
            "for_approval_total": for_approval_total,
            "pending_total": pending_total,
            "completed_total": completed_total,
            "for_approval_orders": for_approval_orders_data.data,
            "pending_orders": pending_orders_data.data,
            "completed_orders": completed_orders_data.data,
            }

        if(_type == "inventory_data"):
            # Inventory Status Overall (Low, Medium and High)
            high_inventory_count = Inventory.objects.filter(available_stock__gte = 20, removed= False).count()
            med_inventory_count = Inventory.objects.filter(available_stock__gte = 10, available_stock__lte = 20, removed= False).count()
            low_inventory_count = Inventory.objects.filter(available_stock__gte = 5, available_stock__lte = 10, removed= False).count()

            high_inventory = Inventory.objects.filter(available_stock__gte = 20, removed= False)
            med_inventory = Inventory.objects.filter(available_stock__gte = 10, available_stock__lte = 20, removed= False)
            low_inventory = Inventory.objects.filter(available_stock__gte = 5, available_stock__lte = 10, removed= False)
            
            high_inventory_data = InventorySerializer(high_inventory, many=True).data
            med_inventory_data = InventorySerializer(med_inventory, many=True).data
            low_inventory_data = InventorySerializer(low_inventory, many=True).data

            # Inventory data (low is less than 50)
            low_inv_overall = Inventory.objects.filter(available_stock__lte = 50, removed= False)[:5] # limit to the top 5
            low_inv_branch1 = Inventory.objects.filter(available_stock__lte = 50, removed= False, branch_id = 2)[:5] # limit to the top 5
            low_inv_branch2 = Inventory.objects.filter(available_stock__lte = 50, removed= False, branch_id = 3)[:5] # limit to the top 5
            low_inv_branch3 = Inventory.objects.filter(available_stock__lte = 50, removed= False, branch_id = 4)[:5] # limit to the top 5

            # Return the inventory data 
            low_inv_overall_data = list(low_inv_overall.values())
            low_inv_branch1_data = list(low_inv_branch1.values())
            low_inv_branch2_data = list(low_inv_branch2.values())
            low_inv_branch3_data = list(low_inv_branch3.values())

            # Number of branch orders and suppliers orders - overall (GROUPED BY MONTH CREATED for each year)
            total_branch_orders = PurchaseHeader.objects.filter(transaction_type = "BRANCH", removed = False,    created_at__year=current_year).annotate(
                                                                    month=TruncMonth('created_at'),
                                                                    month_name=Extract('created_at', 'month')
                                                                ).values(
                                                                    'month',
                                                                    'month_name'
                                                                ).annotate(
                                                                    count=Count('purchase_header_id')
                                                                ).order_by('month')
            # Update month_name for each entry
            for result in total_branch_orders:
                result['month_name'] = result['month'].strftime('%b')

            total_supplier_orders = PurchaseHeader.objects.filter(transaction_type = "SUPPLIER", removed = False,     created_at__year=current_year).annotate(
                                                                    month=TruncMonth('created_at'),
                                                                    month_name=Extract('created_at', 'month')
                                                                ).values(
                                                                    'month',
                                                                    'month_name'
                                                                ).annotate(
                                                                    count=Count('purchase_header_id')
                                                                ).order_by('month')
            # Update month_name for each entry
            for result in total_supplier_orders:
                result['month_name'] = result['month'].strftime('%b')

            response_data = {
                "high_inventory_count": high_inventory_count,
                "med_inventory_count": med_inventory_count,
                "low_inventory_count": low_inventory_count,
                "high_inventory_data": high_inventory_data,
                "med_inventory_data": med_inventory_data,
                "low_inventory_data": low_inventory_data,
                "low_inventory_all": low_inv_overall_data,
                "low_inventory_branch1": low_inv_branch1_data,
                "low_inventory_branch2": low_inv_branch2_data,
                "low_inventory_branch3": low_inv_branch3_data,
                "total_branch_orders": total_branch_orders,
                "total_supplier_orders": total_supplier_orders,
            }

        if response_data:
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Users can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)
        
