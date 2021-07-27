from django.urls import path

from api.views import CompanyViewSet, PeopleViewSet, ListUsers

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Swagger Documentation")

urlpatterns = [
    path("company/<str:name>", CompanyViewSet.as_view()),
    path("people/<int:pk>", PeopleViewSet.as_view()),
    path("people/<int:pk1>/<int:pk2>", ListUsers.as_view()),
    path("swagger/", schema_view, name="openapi-schema"),
]
