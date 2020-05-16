import threading
import datetime
from key_gen_apis.models import Key

WAIT_SECONDS = 60


def scheduler():
    print(f"Scheduler is running! last run at {datetime.datetime.now()}")
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=1)
    queryset = Key.objects.filter(updated_at__gt=time_threshold)
    if queryset:
        # if any item is updated in last 60 seconds means third api used
        pass
    else:
        Key.objects.filter(is_blocked=True).update(is_blocked=False)
    threading.Timer(WAIT_SECONDS, scheduler).start()


# need to start scheduler once when server is start or restart, for that made one endpoint,
# could have used celery but it was third party
