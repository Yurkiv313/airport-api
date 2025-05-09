from rest_framework import viewsets

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
    OrderListSerializer
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

    action_serializers = {
        "list": CountryListSerializer
    }


class CityViewSet(ActionMixin):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    action_serializers = {
        "list": CityListSerializer,
        "retrieve": CityRetrieveSerializer
    }


class CrewViewSet(ActionMixin):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    action_serializers = {
        "list": CrewListSerializer
    }


class AirportViewSet(ActionMixin):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    action_serializers = {
        "list": AirportListSerializer
    }


class RouteViewSet(ActionMixin):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    action_serializers = {
        "list": RouteListSerializer,
        "retrieve": RouteRetrieveSerializer
    }


class AirplaneTypeViewSet(ActionMixin):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ActionMixin):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    action_serializers = {
        "list": AirplaneListSerializer,
        "retrieve": AirplaneRetrieveSerializer
    }


class FlightViewSet(ActionMixin):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    action_serializers = {
        "list": FlightListSerializer,
        "retrieve": FlightRetrieveSerializer
    }


class OrderViewSet(ActionMixin):
    queryset = Order.objects.all()
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
