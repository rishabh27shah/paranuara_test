import os
import json

from django.conf import settings
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand

from api.constants import STORE
from api.models import Company, People


class Command(BaseCommand):
    def handle(self, test=False, *args, **kwargs):
        if test:
            company_resource = os.environ.get(
                "COMPANIES_TEST_RESOURCE_PATH"
            )
            people_resource = os.environ.get(
                "PEOPLE_TEST_RESOURCE_PATH"
            )
        else:
            company_resource = os.environ.get("COMPANIES_RESOURCE_PATH")
            people_resource = os.environ.get("PEOPLE_RESOURCE_PATH")
        with open(settings.BASE_DIR / company_resource) as company_file:
            companies = json.load(company_file)
            for company in companies:
                if not (company.keys() >= {"index", "company"}):
                    print(
                        "Company index and name needed ... Skipped entry"
                    )
                    continue
                try:
                    with transaction.atomic():
                        Company.objects.create(
                            id=company["index"] + 1,
                            company_name=company["company"],
                        )
                except IntegrityError:
                    print(
                        "Duplicate company entry occured with index",
                        company["index"],
                    )
        with open(settings.BASE_DIR / people_resource) as people_file:
            peoples = json.load(people_file)
            temp_peoples = peoples.copy()
            for people in temp_peoples:
                if not ("index" in people):
                    print("People index needed.... entry skipped")
                    peoples.remove(people)
                    continue
                items = {"fruits": [], "vegetables": []}
                for item in people["favouriteFood"]:
                    items[STORE[item]].append(item)
                if not ("company_id" in people):
                    company_id = None
                else:
                    company_id = people["company_id"]
                    try:
                        Company.objects.get(id=company_id)
                    except Company.DoesNotExist:
                        company_id = None
                        print("Company not exist, set to none")
                try:
                    with transaction.atomic():
                        People.objects.create(
                            id=people["index"] + 1,
                            name=people["name"],
                            age=people.get("age", 0),
                            address=people.get("address", ""),
                            phone=people.get("phone", ""),
                            has_died=people.get("has_died", False),
                            eye_color=people.get("eyeColor", ""),
                            fruits=items["fruits"],
                            vegetables=items["vegetables"],
                            company_id=company_id,
                        )
                except IntegrityError:
                    print(
                        "Duplicate People entry occured with index",
                        people["index"],
                    )
            for people in peoples:
                index = people["index"] + 1
                ppl = People.objects.get(id=index)
                frnd_ids = []
                for frnd in people["friends"]:
                    index = frnd["index"] + 1
                    frnd_ids.append(index)
                friends = People.objects.filter(id__in=frnd_ids)
                ppl.friends.add(*friends)
