#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: shuke
@file: response.py 
@time: 2019/10/25 18:16
@contact: shu_ke163@163.com
@software:  swagger-demo
"""

import json

from rest_framework.renderers import JSONRenderer

import logging

logger = logging.getLogger("swagger-demo")


class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'data'
    pagination_object_count = 'count'

    def render(self, data, media_type=None, renderer_context=None):
        response = renderer_context.get('response', None)

        if data.get('results', None) is not None:
            return json.dumps({
                "code": response.status_code,
                "data": data['results'],
                # "count": data['count'],
                "msg": "ok"
            })

        elif data.get('errors', None) is not None:
            return json.dumps({
                "code": response.status_code,
                "msg": data.get('errors')
            })
        else:
            return json.dumps({
                "code": response.status_code,
                "data": data,
                "msg": "ok"
            })
