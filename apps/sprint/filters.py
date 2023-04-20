#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: filters.py 
@time: 2020/01/05 20:12
@software:  swagger-demo
"""

import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = (
            "sprint",
            "status",
            "assigned",
        )


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='iexact')  # iexact表示精确匹配, 并且忽略大小写
    author = django_filters.CharFilter(
        lookup_expr='icontains')  # icontains表示模糊查询（包含），并且忽略大小写
    price = django_filters.NumberFilter(look_expr='exact')  # exact表示精确匹配
    desc = django_filters.CharFilter(
        'description',
        lookup_expr='contains')  # 对'description'字段进行操作，不填默认为desc
    # price__lte = django_filters.NumberFilter('price', lookup_expr='lte') #lte表示小于
    # price__gte = django_filters.NumberFilter('price', look_expr='gte')  # gte表示大于

    # class Meta:
    #     model = Product
    #     fields = ['name', 'author', 'price', 'description']
    #     # fields = {
    #
    # 　            'price': ['lt', 'gt']
    # }
