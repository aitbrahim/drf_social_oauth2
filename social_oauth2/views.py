from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from social_oauth2.utils import psa
from serializers import OAuth2Serializer

from django.shortcuts import render_to_response, redirect


User = get_user_model()


class OAuth2View(generics.CreateAPIView):

    @psa()
    def post(self, request, *args, **kwargs):
        print request
        serializer = OAuth2Serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # The user is populated after the validation went successfully
        return Response({
            'key': serializer.key,
            'id': serializer.user.pk
        })


def home(request):
    """Home view, displays login mechanism"""
    return render_to_response('index.html')
