from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import Account
from apps.account.serializers import LoginSerializer, TokenSerializer, AccountSerializer
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from apps.core.renders import CustomJSONRenderer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging

logger = logging.getLogger("door")


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    user view set
    """

    users_param = openapi.Parameter('page', openapi.IN_QUERY, description="string", type=openapi.TYPE_NUMBER)
    response = openapi.Response('user list', AccountSerializer(many=True))

    @swagger_auto_schema(operation_description='GET /api/v1/account/users/', manual_parameters=[users_param, ],
                         responses={status.HTTP_200_OK: response})
    def list(self, request, *args, **kwargs):
        queryset = Account.objects.filter(is_staff=True).order_by('-id')
        ser = AccountSerializer(queryset, many=True)
        return Response({"code": status.HTTP_200_OK, "data": ser.data})

    @swagger_auto_schema(operation_description='GET /api/v1/account/users/{id}/',
                         responses={status.HTTP_200_OK: "get userinfo success!"})
    def retrieve(self, request, *args, pk=None, **kwargs):
        queryset = Account.objects.filter(id=pk).order_by('-id')
        user = get_object_or_404(queryset, pk=pk)
        ser = AccountSerializer(user)
        return Response({"code": status.HTTP_200_OK, "data": ser.data})


class LoginView(APIView):
    """
    login
    """
    permission_classes = []

    renderer_classes = (CustomJSONRenderer, JSONRenderer)

    # login_response = openapi.Response('login api', TokenSerializer(many=True))

    @swagger_auto_schema(operation_description='POST /api/v1/account/login/', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='string')}
    ), responses={status.HTTP_201_CREATED: f"user create success!"})
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.user

            token, _ = Token.objects.get_or_create(user=user)
            data = TokenSerializer(instance=token).data

            logger.debug(f"{user.username} login success and token: {token}")
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    logout
    """
    permission_classes = []

    # renderer_classes = (CustomJSONRenderer,)
    @swagger_auto_schema(operation_description='GET /api/v1/account/logout/',
                         responses={status.HTTP_200_OK: "user logout"})
    def get(self, request, *args, **kwargs):
        try:
            token = request.user.auth_token.key
            request.user.auth_token.delete()
            logger.debug(f"{request.user} logout and token: {token}")
            return Response(data={"code": status.HTTP_200_OK, "msg": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.debug(f"{request.user} logout failed: {str(e)}")
            return Response(data={"errors": f"{e.__class__.__name__}: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordView(APIView):
    """
    reset password
    """

    @swagger_auto_schema(operation_description='POST /api/v1/account/reset/',
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                             'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                             'repeat_password': openapi.Schema(type=openapi.TYPE_STRING, description='string')}),
                         responses={status.HTTP_201_CREATED: f"reset password success!"})
    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        repeat_password = request.data.get('repeat_password', None)
        res = {"code": status.HTTP_200_OK, "msg": "ok"}
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
