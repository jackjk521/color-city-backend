from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Branch
from ..serializers import BranchSerializer

# Branch 
class BranchApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the branches
        '''
        branches = Branch.objects.filter(removed = False).order_by('branch_id')
        serializer = BranchSerializer(branches, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Branches can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Branch with given Branch Data
        '''
        data = {
            'branch_name': request.data.get('branch_name'),  
            'address': request.data.get('address'), 
        }

        serializer = BranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message' : "Error saving branch data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BranchDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, branch_id):
        '''
        Helper method to get the object with given branch_id
        '''
        try:
            return Branch.objects.get(branch_id=branch_id)
        except Branch.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, branch_id, *args, **kwargs):
        '''
        Retrieves the Branch with given branch_id
        '''
        branch_instance = self.get_object(branch_id)
        if not branch_instance:
            return Response(
                {"message": "Branch with the branch id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BranchSerializer(branch_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, branch_id,  *args, **kwargs):
        '''
        Updates the Branch item with given branch_id if exists
        '''
        branch_instance = self.get_object(branch_id)
        if not branch_instance:
            return Response(
                {"message": "Branch with that branch id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
           
        data = {
            'branch_name': request.data.get('branch_name'), 
            'address': request.data.get('address'), 
        }

        serializer = BranchSerializer(instance = branch_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
            branch_instance.branch_name = serializer.validated_data['branch_name']
            branch_instance.address = serializer.validated_data['address']
            branch_instance.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'message' : "Error updating branch data", 'errors' : serializer.errors}, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete (Soft Delete)
    def delete(self, request, branch_id, *args, **kwargs):
        '''
        Deletes the Branch item with given branch_id if exists
        '''
        branch_instance = self.get_object(branch_id)
        if not branch_instance:
            return Response(
                {"message": "Branch with that branch id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update the "removed" column to True
        branch_instance.removed = True  
        branch_instance.save()

        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    