from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from pets.serializers import PetSerializer
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        group_obj = Group.objects.filter(
                scientific_name__iexact=group_data["scientific_name"]
            ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for trait in traits_data:
            """ import ipdb; ipdb.set_trace() """
            trait_filter = Trait.objects.filter(
                name__iexact=trait["name"]
            ).first()

            if not trait_filter:
                trait_filter = Trait.objects.create(**trait)
            pet.traits.add(trait_filter)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        if request.query_params:
            name_trait = request.query_params.get("trait", None)
            pet = Pet.objects.filter(traits__name__iexact=name_trait)
        else:
            pet = Pet.objects.all()
        result_page = self.paginate_queryset(pet, request)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetInfoView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            group_obj = Group.objects.filter(
                scientific_name__iexact=group_data["scientific_name"]
            ).first()

            if not group_obj:
                group_obj = Group.objects.create(**group_data)

            pet.group = group_obj

        if traits_data:
            traits_list = []
            for trait in traits_data:
                trait_filter = Trait.objects.filter(
                    name__iexact=trait["name"]).first()
                if not trait_filter:
                    trait_filter = Trait.objects.create(**trait)
                traits_list.append(trait_filter)
            pet.traits.set(traits_list)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
