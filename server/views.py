import binascii
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from server import settings
from .models import User, Seller
from .serializers import UserSerializer, SellerSerializer
from rest_framework.permissions import IsAuthenticated
import base64
from rest_framework.exceptions import ParseError
import os

def decode_and_save_image(base64image,username):
    """Decodes the base64 image data and saves it to the Django media file."""
    try:
        # Remove the data type from the base64 image data if present
        base64_data = base64image.split(',')[-1]
        # Decode the base64 data
        image_data = base64.b64decode(base64_data)
    except (IndexError, TypeError, binascii.Error) as e:
        raise ParseError(detail="Invalid image data format")

    # Generate a unique filename for the image
    file_name = f"identity_piece_{username}_{os.urandom(4).hex()}.png"

    # Define the media directory where the image will be saved
    media_directory = os.path.join(settings.MEDIA_ROOT, "identity_images")

    # Check if the media directory exists, if not create it
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    # Create the file path for the image
    file_path = os.path.join(media_directory, file_name)

    # Open the file in binary write mode and save the image data
    with open(file_path, 'wb') as f:
        f.write(image_data)

    return file_path


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def migrate_to_seller(request):
    user = request.user
    if user.is_seller:
        return Response("User is already a seller", status=status.HTTP_400_BAD_REQUEST)
    else:
        identity_piece_data = request.data['identity_piece']
        # Assuming the base64 data is after the first comma (',') in the data.
        # You may need to adjust this based on your specific data format.
        base64_data = identity_piece_data.split('=')[0] + "="

        try:
            file_path = decode_and_save_image(base64_data,request.data['username'])
            print(file_path)
        except ParseError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Now you have the file_path where the image is saved in the media directory.
        # You can use it to further process or save the Seller instance.

        return Response("workin on it")
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")