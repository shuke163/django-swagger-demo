#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shuke
@file: baseviews.py 
@time: 2019/10/26 17:47
@contact: shu_ke163@163.com
@software:  Door
"""

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class ReturnFormatMixin(object):

    @classmethod
    def get_ret(cls):
        return {'status': 0, 'msg': '', 'data': {}}


class BasePagination(PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000


class DefaultPagination(BasePagination):
    page_size = 10


class MaxSizePagination(BasePagination):
    page_size = 1000


class BaseView(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    # 分页
    pagination_class = DefaultPagination
    # 搜索
    filter_backends = [filters.SearchFilter]
    search_fields = []
