# celery的任务必须写在tasks.py的文件中，别的文件名称不识别!!!
from mycelery.main import app
from luffyapi.libs.yuntongxun.sms import CCP
from luffyapi.settings import constants
import logging

log = logging.getLogger('django')


@app.task  # name表示设置任务的名称，如果不填写，则默认使用函数名做为任务名
def send_sms(mobile, sms_code):
    ccp = CCP()
    ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
    if ret == -1:
        log.error("短信发送失败![CCP] 手机号:%s" % mobile)

