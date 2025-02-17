#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020-07-06 10:24:59
# @Remarks  : 包含home_application用到的所有装饰器
from django.http import JsonResponse

from home_application.models import GroupUser
from home_application.utils.iam_util import IAMClient


def is_group_member(admin_needed: list = None):
    """
    判断是否为对应组的成员或者管理员
    默认情况下判断是否为组内成员，若是需要管理员权限则将请求方法加在admin_needed中
    :param admin_needed: 需要管理员权限的方法
    :return: 经过views中响应逻辑函数处理后的http结果
    """
    if admin_needed is None:
        admin_needed = []

    def wrapper(func):
        def inner(request, *args, **kwargs):
            group_id = kwargs["group_id"]
            username = request.user.username
            if request.method in admin_needed:
                # 判断是否具有管理员权限
                if IAMClient().allowed_manage_group(username, group_id):
                    return func(request, *args, **kwargs)
                else:
                    return JsonResponse({"result": False, "code": -1, "message": "您没有权限管理该组，请联系组管理员", "data": []})
            else:
                # 判断是否为当前组的组员
                try:
                    GroupUser.objects.get(group_id=group_id, user_id=request.user.id)
                    return func(request, *args, **kwargs)
                except GroupUser.DoesNotExist:
                    return JsonResponse({"result": False, "code": -1, "message": "您不在对应的组", "data": []})

        return inner

    return wrapper
