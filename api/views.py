import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView

from .models import Company, People
from .serializers import (
    PeopleSerializer,
    PeopleDetailSerializer,
    PeopleCustomSerializer,
)


class CompanyViewSet(generics.ListAPIView):
    """
        Return details of employees working in a company.
    """

    model = Company
    serializer_class = PeopleSerializer

    def get_queryset(self, *args, **kwargs):
        """
        get_queryset : customise queryset
        """
        company = self.kwargs["name"]
        company_object = get_object_or_404(
            Company, company_name=company
        )
        employees = company_object.people_set.all()
        return employees


class PeopleViewSet(APIView):
    """
        Return details of People like name, age, fruits,
        vegetables.
    """

    def get(self, request, *args, **kwargs):
        """
        get : Person Details
        """
        people_id = self.kwargs["pk"]
        obj = get_object_or_404(People, id=people_id)
        serialised = PeopleCustomSerializer(obj)
        return HttpResponse(json.dumps(serialised.data))


class ListUsers(APIView):
    """
        Return detail of both users and list of their common
        friends with brown eyes and they are still alive.
    """

    def get(self, request, *args, **kwargs):
        """
        get : Details of both users along with their comman friends with brown eyes and still alive.
        """
        people_id1 = self.kwargs["pk1"]
        people_id2 = self.kwargs["pk2"]
        obj1 = get_object_or_404(People, id=people_id1)
        obj2 = get_object_or_404(People, id=people_id2)
        obj1_friends = obj1.friends.values_list("pk", flat=True)
        mutual_friends = obj2.friends.filter(
            pk__in=obj1_friends, has_died=False, eye_color="brown"
        )
        serialised = PeopleDetailSerializer(mutual_friends, many=True)
        person1 = PeopleDetailSerializer(obj1)
        person2 = PeopleDetailSerializer(obj2)
        data = {
            "person1": person1.data,
            "person2": person2.data,
            "common_friends": serialised.data,
        }
        return HttpResponse(json.dumps(data))
