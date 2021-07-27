from rest_framework import serializers

from .models import Company, People


class PeopleSerializer(serializers.ModelSerializer):
    """
    PeopleSerializer : fields all
    """

    class Meta:
        model = People
        fields = "__all__"


class PeopleDetailSerializer(serializers.ModelSerializer):
    """
    PeopleDetailSerializer : fields id, name, age, address,
    phone, fruits, vegetables
    """

    class Meta:
        model = People
        fields = (
            "name",
            "age",
            "address",
            "phone"
        )


class CompanySerializer(serializers.ModelSerializer):
    """
    CompanySerializer : fields all
    """

    class Meta:
        model = Company
        fields = "__all__"


class PeopleCustomSerializer(serializers.ModelSerializer):
    """
    PeopleDetailSerializer : fields username, age, fruits, vegetables
    """
    username = serializers.SerializerMethodField('get_alternate_name')

    class Meta:
        model = People
        fields = (
            "username",
            "age",
            "fruits",
            "vegetables",
        )

    def get_alternate_name(self, obj):
        return obj.name