import json

from rest_framework import status
from rest_framework.test import APITestCase

from api.management.commands import loaddata
from .models import Company, People
from .serializers import (
    PeopleSerializer,
    PeopleDetailSerializer,
    PeopleCustomSerializer,
)


class APITest(APITestCase):
    """
        APITest : for testing API endpoints.
    """

    def setUp(self):
        cmd = loaddata.Command()
        opts = {"test": True}
        cmd.handle(**opts)

    def test_company_employee(self):
        """
        test_company_employee : test /company/<name>/ endpoint
        """
        company_object = Company.objects.all().first()
        respone = self.client.get(
            "/company/" + company_object.company_name
        )
        employees = company_object.people_set.all()
        serialized_employee = PeopleSerializer(employees, many=True)
        self.assertEqual(respone.data, serialized_employee.data)
        self.assertEqual(respone.status_code, status.HTTP_200_OK)

    def test_people_detail(self):
        """
        test_company_detail : test /people/<pk>/ endpoint
        """
        people_object = People.objects.all().first()
        respone = self.client.get("/people/" + str(people_object.id))
        serialized_people = PeopleCustomSerializer(people_object)
        self.assertEqual(
            respone.content.decode("UTF-8"),
            json.dumps(serialized_people.data),
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)

    def test_people_detail_common_friends(self):
        """
        test_people_detail_common_friends : test 
        /people/<pk>/<pk>/ endpoint
        """
        people = People.objects.all()
        obj1 = people[0]
        obj2 = people[1]
        respone = self.client.get(
            "/people/" + str(obj1.id) + "/" + str(obj2.id)
        )
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
        self.assertEqual(
            json.loads(respone.content.decode("UTF-8")), data
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
