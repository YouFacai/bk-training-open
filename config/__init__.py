# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from __future__ import absolute_import

import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from blueapps.core.celery import celery_app

__all__ = ["celery_app", "RUN_VER", "APP_CODE", "SECRET_KEY", "BK_URL", "BASE_DIR"]


# app 基本信息


def get_env_or_raise(key):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(
            ('Environment variable "{}" not found, you must set this variable to run this application.').format(key)
        )
    return value


# 应用 ID
APP_CODE = get_env_or_raise("BKAPP_APP_CODE")
# 应用用于调用云 API 的 Secret
SECRET_KEY = get_env_or_raise("BKAPP_APP_SECRET")

# SaaS运行版本，如非必要请勿修改
RUN_VER = "open"
# 蓝鲸SaaS平台URL，例如 http://paas.bking.com
# 不要直接拿来用，测试环境和正式环境会在后边拼接'/console/'    见blueapps/patch/settings_open_saas.py 79行
# 如需蓝鲸SaaS平台URL，可以使用settings.BKAPP_PAAS_URL     见config.default.py 140行
BK_URL = "https://paas-edu.bktencent.com:443"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
