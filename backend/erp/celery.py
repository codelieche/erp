"""
使用方式：
1. 进入项目源码目录
2. 启动Celery：celery -A erp worker -l info
"""

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')

app = Celery('erp')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
