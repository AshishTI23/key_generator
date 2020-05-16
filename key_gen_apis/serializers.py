from rest_framework import serializers
from key_gen_apis.models import Key


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = "__all__"


def xyx():
    print("hiiiiiiiiiii")
