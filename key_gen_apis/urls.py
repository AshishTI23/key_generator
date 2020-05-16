from django.urls import path
from key_gen_apis.views import CreateUpdateDeleteKey, SchedulerApi

urlpatterns = [
    path("random_api_key/", CreateUpdateDeleteKey.as_view()),
    path("start_scheduler/", SchedulerApi.as_view()),
]
