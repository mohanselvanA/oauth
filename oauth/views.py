from rest_framework.decorators import APIView
from django.contrib.auth.models import User
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import get_access_token
import boto3
# from botocore.exceptions import ClientError

# serializers
from .serializers import UserSerializer


# user can able to login 

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            
            if user.check_password(password):
            
                tokens = get_access_token(user)
                return Response(tokens)
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
        except User.DoesNotExist:
            return Response({'error': "please enter the user details"}, status=status.HTTP_400_BAD_REQUEST)
        
        

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # users = User.objects.all()
        # serializer = UserSerializer(users, many=True)
        return Response({'message': "hello"}, status=status.HTTP_200_OK)
    

# uses boto3 to access all the information from aws cloud
    

class GetAllInstancesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ec2_client = boto3.client('ec2', region_name='ap-south-1')

        try:
            response = ec2_client.describe_instances()

            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_details = {
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                    }
                    instances.append(instance_details)

            return Response({'instances': instances}, status=status.HTTP_200_OK)

        # except ClientError as e:
        #     error_message = f"AWS API Error: {str(e)}"
        #     return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





