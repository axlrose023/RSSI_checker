import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RSSI.settings')
from celery import Celery
from RSSI import settings

app = Celery('RSSI')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def rssi_show_dicts():
    sensors = ['R407', 'RNGU', 'R401', 'R403', 'R301', 'R502', 'R508', 'R514', 'R403s1', 'R405', 'R415', 'R420']
    for sensor in sensors:
        from RSSI.rssi_utils.updater import get_sensor
        lines, more = get_sensor(sensor)
        from run.models import RssiDataLess
        RssiDataLess.objects.create(host=sensor, data=lines)
        from run.models import RssiDataMore
        RssiDataMore.objects.create(host=sensor, data=more)


@app.task()
def return_hello():
    print('Hello World!')
