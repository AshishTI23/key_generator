from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from key_gen_apis.scheduler import scheduler
from rest_framework.generics import get_object_or_404
from key_gen_apis.serializers import KeySerializer
from django.db.models import Q
from key_gen_apis.models import Key
import datetime
import string
import random
import threading


class UpdateAliveAndBlockStatus(threading.Thread):
    """
    purpose: Thread to update last used time of key and block the key
    """

    def __init__(self, key, new_alive_time):
        self.key = key
        self.new_alive_time = new_alive_time
        threading.Thread.__init__(self)

    @staticmethod
    def block_and_update_new_alive_time(key, new_alive_time):
        key_object = get_object_or_404(Key.objects.all(), api_key=key)
        key_object.is_blocked = True
        key_object.alive = new_alive_time
        key_object.save()

    def run(self):
        self.block_and_update_new_alive_time(self.key, self.new_alive_time)


class CreateUpdateDeleteKey(APIView):
    """
    purpose: To generate random API key, fetch one key which is not being used anywhere,
            update key status (is_blocked=False), delete key (hard delete)
    """

    def post(self, request):
        key = self.random_api_key()
        data = dict()
        data["api_key"] = key
        serializer = KeySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=5)
        queryset = Key.objects.filter(
            Q(alive=None) | Q(alive__lt=time_threshold)
        ).filter(is_blocked=False)
        if queryset:
            random_idx = random.randint(0, queryset.count() - 1)
            random_object = queryset[random_idx]
            serializer = KeySerializer(random_object)
            new_alive_time = datetime.datetime.now()
            UpdateAliveAndBlockStatus(random_object.api_key, new_alive_time).start()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "No available key found"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request):
        key_to_be_unblocked = request.query_params.get("api_key")
        if key_to_be_unblocked is not None:
            key_object = get_object_or_404(
                Key.objects.all(), api_key=key_to_be_unblocked
            )
            serializer = KeySerializer(
                instance=key_object, data={"is_blocked": False}, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Kindly send key to be updated, given key does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        key_to_be_deleted = request.query_params.get("api_key")
        if key_to_be_deleted is not None:
            key_object = get_object_or_404(Key.objects.all(), api_key=key_to_be_deleted)
            if key_object:
                key_object.delete()
            return Response(
                {"message": "Given key has been deleted"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Kindly send key to be deleted, given key does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def random_api_key(string_length=20):
        """Generate a random string of letters and digits """
        letters_and_digits = string.ascii_letters + string.digits
        key = "".join(random.choice(letters_and_digits) for i in range(string_length))
        return str(key).strip()


class SchedulerApi(APIView):
    """
    purpose: to run a function in every 60 seconds
    """

    def get(self, request):
        scheduler()
        return Response(
            {
                "message": "Scheduler has been started to unblock keys at "
                "given condition, Kindly do not hit again "
            },
            status=status.HTTP_200_OK,
        )
