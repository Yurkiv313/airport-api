from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    Airplane,
    Flight,
    Order,
    AirplaneType,
    Crew
)
from airport_app.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
    FlightSerializer,
    OrderSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    OrderRetrieveSerializer,
    CountryListSerializer,
    CityListSerializer,
    CityRetrieveSerializer,
    CrewListSerializer,
    AirportListSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderListSerializer,
    CrewRetrieveSerializer,
    AirportRetrieveSerializer
)


class ActionMixin(viewsets.ModelViewSet):
    action_serializers = {}

    def get_serializer_class(self):
        if self.action_serializers and self.action in self.action_serializers:
            return self.action_serializers[self.action]
        return super().get_serializer_class()


class CountryViewSet(ActionMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    action_serializers = {
        "list": CountryListSerializer
    }


class CityViewSet(ActionMixin):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['country']
    search_fields = ["name"]

    action_serializers = {
        "list": CityListSerializer,
        "retrieve": CityRetrieveSerializer
    }


class CrewViewSet(ActionMixin):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["position"]
    search_fields = ["search_full_name"]

    action_serializers = {
        "list": CrewListSerializer,
        "retrieve": CrewRetrieveSerializer
    }

    def get_queryset(self):
        return Crew.objects.annotate(
            search_full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
                output_field=CharField()
            )
        )


class AirportViewSet(ActionMixin):
    queryset = Airport.objects.select_related("city", "city__country")
    serializer_class = AirportSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['city', "city__country"]
    search_fields = ["name"]

    action_serializers = {
        "list": AirportListSerializer,
        "retrieve": AirportRetrieveSerializer
    }


class RouteViewSet(ActionMixin):
    queryset = Route.objects.select_related(
        "source",
        "source__city",
        "source__city__country",
        "destination",
        "destination__city",
        "destination__city__country"
    )
    serializer_class = RouteSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['source', "destination"]
    search_fields = ["source__name", "destination__name"]

    action_serializers = {
        "list": RouteListSerializer,
        "retrieve": RouteRetrieveSerializer
    }


class AirplaneTypeViewSet(ActionMixin):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class AirplaneViewSet(ActionMixin):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["airplane_type"]
    search_fields = ["name"]

    action_serializers = {
        "list": AirplaneListSerializer,
        "retrieve": AirplaneRetrieveSerializer
    }


class FlightViewSet(ActionMixin):
    queryset = Flight.objects.select_related(
        "route__source",
        "route__destination",
        "route__source__city",
        "route__destination__city",
        "route__source__city__country",
        "route__destination__city__country",
        "airplane"
    ).prefetch_related("crew")
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["route", "airplane", "is_active", "departure_time", "arrival_time"]
    search_fields = ["route__source__name", "route__destination__name"]

    action_serializers = {
        "list": FlightListSerializer,
        "retrieve": FlightRetrieveSerializer
    }


class OrderViewSet(ActionMixin):
    queryset = Order.objects.prefetch_related("tickets")
    serializer_class = OrderSerializer

    action_serializers = {
        "list": OrderListSerializer,
        "retrieve": OrderRetrieveSerializer
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
