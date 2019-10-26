from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import Account
from apps.account.serializers import LoginSerializer, TokenSerializer, AccountSerializer
from rest_framework import viewsets
from libs.renders import CustomJSONRenderer
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger("door")


class AccountViewSet(viewsets.ViewSet):
    """
    user view set
    """

    def list(self, request, *args, **kwargs):
        queryset = Account.objects.filter(is_staff=True).order_by('-id')
        ser = AccountSerializer(queryset, many=True)
        return Response({"code": status.HTTP_200_OK, "data": ser.data})

    def retrieve(self, request, *args, pk=None, **kwargs):
        queryset = Account.objects.filter(id=pk).order_by('-id')
        user = get_object_or_404(queryset, pk=pk)
        ser = AccountSerializer(user)
        return Response({"code": status.HTTP_200_OK, "data": ser.data})


class LoginView(APIView):
    """
    login
    """
    # serializer_class = LoginSerializer
    permission_classes = []

    renderer_classes = (CustomJSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user

            token, _ = Token.objects.get_or_create(user=user)
            data = TokenSerializer(token).data

            logger.debug(f"{user.username} login success and token: {token}")
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(APIView):
    """
    重置密码
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        repeat_password = request.data.get('repeat_password', None)
        res = {"code": status.HTTP_200_OK, "message": "ok"}
        if user.check_password(old_password):
            if not new_password:
                res["message"] = "The new password cannot be empty"
            if new_password != repeat_password:
                res["message"] = "The two passwords do not match"
            else:
                user.set_password(new_password)
                user.save()
                logger.info(f"The user {user.username} set password success")
            return Response(data=res)
        else:
            res["message"] = "Original password error"
            return Response(data=res)
