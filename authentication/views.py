from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
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

        return Response(user_data, status=status.HTTP_201_CREATED)