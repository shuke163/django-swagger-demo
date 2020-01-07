#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: views.py 
@time: 2020/01/05 15:55
@software:  Door
"""

from django.contrib.auth import get_user_model

from rest_framework import authentication, permissions, filters
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from rest_framework.renderers import JSONRenderer
from apps.core.renders import CustomJSONRenderer

from rest_framework.response import Response

from .models import Sprint, Task
from .serializers import SprintSerializers, TaskSerializer, UserSerializers

from .filters import TaskFilter

User = get_user_model()


class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permissions_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
        A simple ViewSet for listing or retrieving users.
    """
    serializer_class = SprintSerializers
    renderer_classes = (CustomJSONRenderer, JSONRenderer)
    search_fields = ("name",)
    ordering_fields = ("end", "name",)

    def list(self, request, *args, **kwargs):
        queryset = Sprint.objects.all().order_by("end")
        ser = SprintSerializers(queryset, many=True)
        return Response({"data": ser.data})

    def retrieve(self, request, version, pk=None):
        queryset = Sprint.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        ser = SprintSerializers(user)
        return Response(ser.data)


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    filter_class = TaskFilter
    serializer_class = TaskSerializer
    search_fields = ("name", "description",)
    ordering_fields = ("name", "order", "started", "due", "completed",)


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializers
    search_fields = (User.USERNAME_FIELD,)
