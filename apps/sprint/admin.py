#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: admin.py 
@time: 2020/01/06 10:05
@software:  Door
"""

from django.contrib import admin
from apps.sprint import models

admin.site.register(models.Sprint)
admin.site.register(models.Task)
