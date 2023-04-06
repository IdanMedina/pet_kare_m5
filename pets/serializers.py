from rest_framework import serializers
from .models import SexPet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(default=None)
    weight = serializers.FloatField(default=None)
    sex = serializers.ChoiceField(
        max_length=20, choices=SexPet.choices, default=SexPet.NOT_INFORMED)

    group = GroupSerializer()
    traits = TraitSerializer(many=True, read_only=True, default=None)
