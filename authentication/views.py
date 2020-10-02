from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

import jwt
from decouple import config

from .models import User
from .utils import Util
from .serializers import RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data=user)
        # it will validate w/ help of validate() in serializer
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user_data = serializers.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        abs_url = 'https://'+current_site+relative_link+"?token="+str(token)

        email_body = 'Hi '+user.username + \
                     '\n Use Link Below To Verify Your Email.\n' + \
                     abs_url + '\n Thank You For Being with Us.'

        data = {'email_subject': 'Verify Your Email',
                'email_body': email_body,
                'email_to': user.email}

        Util.send_mail(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, config('SECRET_KEY'))
            user = User.objects.get(id=payload['user_id'])
            if not user.is_varified:
                user.is_varified = True
                user.save()
            return Response({'message': 'Successfully Activated'}, status=status.HTTP_202_ACCEPTED)

        except jwt.ExpiredSignatureError as ex:
            return Response({'error': 'Activation Link Expired'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as ex:
            return Response({'error': 'Invalid Token'},
                            status=status.HTTP_400_BAD_REQUEST)