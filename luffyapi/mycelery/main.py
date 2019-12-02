# 主程序
from celery import Celery
import os
import django

# 创建celery实例对象
app = Celery("luffy")

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'luffyapi.settings.dev')
django.setup()


# 通过app对象加载配置
app.config_from_object("mycelery.config")

# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["mycelery.sms", "mycelery.mail"])

# 启动Celery的命令
# 强烈建议切换目录到项目的根目录下启动celery!!
# celery -A mycelery.main worker --loglevel=info
# windows下:
# celery -A mycelery.main worker --loglevel=info --pool=gevent
