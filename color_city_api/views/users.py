import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.middleware import SessionMiddleware


# User Auth
class UserAuthApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. Get valid user
    def post(self, request, *args, **kwargs):
        '''
        Get user with valid credentials
        '''
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            user_data = {
                'user_id': user.user_id,
                'branch': user.branch_id, # foreign key
                'branch_name': user.branch_name,
                'username': user.username,
                'password': user.password,
                'user_role': user.user_role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                # Include any other desired user data
            }

            #  # Save user_data to the session
            # session_middleware = SessionMiddleware(get_response=None)
            # session_middleware.process_request(request)

            # Save user_data to the session
            request.session['user_data'] =  {
                'user_id': user.user_id,
                'branch': user.branch_id, # foreign key
                'branch_name': user.branch_name,
                'username': user.username,
                'password': user.password,
                'user_role': user.user_role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                # Include any other desired user data
            }
            request.session.save()

            serializer = UserSerializer(instance = user, data=user_data)

            if serializer.is_valid():
                # Check if the provided password matches the stored password
                if user.password != password:  # Assuming the password is stored as plain text
                    return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# User
class UserApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]

    # 1. List all (get all)
    def get(self, request, *args, **kwargs):
        '''
        List all the users
        '''
        users = User.objects.filter(removed = False).order_by('user_id')
        serializer = UserSerializer(users, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Users can not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)
        

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the User with given User Data
        '''
        data = {
            'branch': request.data.get('branch'),  # foreign key
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'user_role': request.data.get('user_role'), 
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'age': request.data.get('age'),
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # If valid, then save user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Else, throw an error
        return Response({'message' : "Error saving user data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                {"message": "User with that user id does not exist"},
                status=status.HTTP_404_NOT_FOUND
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
                {"message": "User with that user id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
           
        data = {
            'branch': request.data.get('branch'),  # foreign key    
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'user_role': request.data.get('user_role'), 
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'age': request.data.get('age'),
        }

        serializer = UserSerializer(instance = user_instance, data=data, partial = True)

        if serializer.is_valid():
            # Update the fields of the item object
            user_instance.branch = serializer.validated_data['branch']
            user_instance.username = serializer.validated_data['username']
            user_instance.password = serializer.validated_data['password']
            user_instance.user_role = serializer.validated_data['user_role']
            user_instance.first_name = serializer.validated_data['first_name']
            user_instance.last_name = serializer.validated_data['last_name']
            user_instance.age = serializer.validated_data['age']

            user_instance.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message": "Error updating user data", 'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                        
    # 5. Delete (Soft Delete)
    def delete(self, request, user_id, *args, **kwargs):
        '''
        Deletes the User item with given user_id if exists
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"message": "User with that user id does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update the "removed" column to True
        user_instance.removed = True  
        user_instance.save()
        
        return Response(
            {"message": "Successfully removed user"},
            status=status.HTTP_200_OK
        )