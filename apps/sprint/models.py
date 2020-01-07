#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: models.py 
@time: 2020/01/05 15:43
@software:  Door
"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Sprint(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    end = models.DateField(unique=True)

    def __str__(self):
        return self.name or _("Sprint ending".format(self.end))


class Task(models.Model):
    STATUS_TODO = 1
    STATUS_IN_PROGRESS = 2
    STATUS_TESTING = 3
    STATUS_DONE = 4

    STATUS_CHOICE = (
        (STATUS_TODO, _('Not Started')),
        (STATUS_IN_PROGRESS, _('In pProgress')),
        (STATUS_TESTING, _("Testing")),
        (STATUS_DONE, _("Done")),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='sprint', blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=STATUS_TODO)
    order = models.SmallIntegerField(default=0)
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    started = models.DateField(blank=True, null=True)
    due = models.DateField(blank=True, null=True)
    completed = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
