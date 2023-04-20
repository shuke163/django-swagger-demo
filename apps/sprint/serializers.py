#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: serializers.py 
@time: 2020/01/05 15:53
@software:  swagger-demo
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import reverse
from .models import Sprint, Task

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            User.USERNAME_FIELD,
            "full_name",
            "is_active",
        )

    def get_links(self, obj):
        request = self.context["request"]
        username = obj.get_username()
        return {
            "self":
            reverse("user-detail",
                    kwagrs={User.USERNAME_FIELD: username},
                    request=request),
        }


class SprintSerializers(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = ("id", "name", "description", "end", "links")

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self":
            reverse("sprint-detail", kwagrs={"pk": obj.pk}, request=request),
        }


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,
                                            required=False,
                                            allow_null=True,
                                            queryset=User.objects.all)
    status_display = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ("id", "name", "description", "sprint", "status",
                  "status_display", "order", "assigned", "started", "due",
                  "completed", "links")

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self": reverse("task-detail",
                            kwargs={"pk": obj.pk},
                            request=request)
        }
