from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import User
from ..serializers import UserSerializer
from django.shortcuts import get_object_or_404

# User 
class UserApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the users
        '''
        users = User.objects.filter(removed = False).order_by('user_id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the User with given User Data
        '''
        data = {
            'branch': request.data.get('branch'),  # foreign key
            'user_role': request.data.get('user_role'), 
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'age': request.data.get('age'),
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailApiView(APIView):

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user_id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

    # 3. Get Specific 
    def get(self, request, user_id, *args, **kwargs):
        '''
        Retrieves the User with given user_id
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "User with User id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, user_id,  *args, **kwargs):
        '''
        Updates the User item with given user_id if exists
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with User id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
           
        data = {
            'branch': request.data.get('branch'),  # foreign key
            'user_role': request.data.get('user_role'), 
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'age': request.data.get('age'),
        }

        serializer = UserSerializer(instance = user_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
                user_instance.branch = serializer.validated_data['branch']
                user_instance.user_role = serializer.validated_data['user_role']
                user_instance.first_name = serializer.validated_data['first_name']
                user_instance.last_name = serializer.validated_data['last_name']
                user_instance.age = serializer.validated_data['age']

                # Call the update() method on the queryset to update the item
                User.objects.filter(user_id=user_id).update(
                    branch=user_instance.branch,
                    user_role=user_instance.user_role,
                    first_name=user_instance.first_name,
                    last_name= user_instance.last_name,
                    age= user_instance.age  ,                                 
                    # Update other fields as needed
                )

                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400__BAD_REQUEST)
                        
    # 5. Delete
    def delete(self, request, user_id, *args, **kwargs):
        '''
        Deletes the User item with given user_id if exists
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with User id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    def soft_delete(self, request, user_id, *args, **kwargs):
        '''
        Soft deletes the User with the given user_id if it exists
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with User id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_instance.removed = True  # Update the "removed" column to True
        user_instance.save()

        return Response(
            {"res": "Object soft deleted!"},
            status=status.HTTP_200_OK
        )
    