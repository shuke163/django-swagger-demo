#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: urls.py 
@time: 2020/01/06 10:01
@software:  Door
"""
from django.conf.urls import url, include
from apps.sprint.views import *
from rest_framework.routers import DefaultRouter

user_list = SprintViewSet.as_view({'get': 'list'})
user_detail = SprintViewSet.as_view({'get': 'retrieve'})

router = DefaultRouter(trailing_slash=False)
router.register(r'sprint', SprintViewSet, basename='sprint')

urlpatterns = [
    url(r'^', include(router.urls)),
]
