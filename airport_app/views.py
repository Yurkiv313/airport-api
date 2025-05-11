from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    Airplane,
    Flight,
    Order,
    AirplaneType,
    Crew,
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
    AirportRetrieveSerializer, AirplaneImageSerializer,
)


class ActionMixin(viewsets.ModelViewSet):
    action_serializers = {}

    def get_serializer_class(self):
        if self.action_serializers and self.action in self.action_serializers:
            return self.action_serializers[self.action]
        return super().get_serializer_class()


class CustomPermissionMixin(viewsets.ModelViewSet):
    action_permissions = {}

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "upload_image"]:
            if (
                    self.__class__.__name__ == "OrderViewSet"
                    and self.action == "create"
            ):
                return [IsAuthenticated()]
            return [IsAdminUser()]

        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [IsAdminUser]
            )
        ]


class CountryViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    action_serializers = {"list": CountryListSerializer}

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
    }


class CityViewSet(ActionMixin, CustomPermissionMixin):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["country"]
    search_fields = ["name"]

    action_serializers = {
        "list": CityListSerializer,
        "retrieve": CityRetrieveSerializer,
    }

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
    }


class CrewViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["position"]
    search_fields = ["search_full_name"]

    action_serializers = {
        "list": CrewListSerializer,
        "retrieve": CrewRetrieveSerializer,
    }

    action_permissions = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
    }

    def get_queryset(self):
        return Crew.objects.annotate(
            search_full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
                output_field=CharField(),
            )
        )


class AirportViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Airport.objects.select_related("city", "city__country")
    serializer_class = AirportSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["city", "city__country"]
    search_fields = ["name"]

    action_serializers = {
        "list": AirportListSerializer,
        "retrieve": AirportRetrieveSerializer,
    }

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
    }


class RouteViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Route.objects.select_related(
        "source",
        "source__city",
        "source__city__country",
        "destination",
        "destination__city",
        "destination__city__country",
    )
    serializer_class = RouteSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["source", "destination"]
    search_fields = ["source__name", "destination__name"]

    action_serializers = {
        "list": RouteListSerializer,
        "retrieve": RouteRetrieveSerializer,
    }

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
    }


class AirplaneTypeViewSet(ActionMixin, CustomPermissionMixin):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    action_permissions = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
    }


class AirplaneViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["airplane_type"]
    search_fields = ["name"]

    action_serializers = {
        "list": AirplaneListSerializer,
        "retrieve": AirplaneRetrieveSerializer,
        "upload_image": AirplaneImageSerializer
    }

    action_permissions = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
    }

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Flight.objects.select_related(
        "route__source",
        "route__destination",
        "route__source__city",
        "route__destination__city",
        "route__source__city__country",
        "route__destination__city__country",
        "airplane",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "route",
        "airplane",
        "is_active",
        "departure_time",
        "arrival_time",
    ]
    search_fields = ["route__source__name", "route__destination__name"]

    action_serializers = {
        "list": FlightListSerializer,
        "retrieve": FlightRetrieveSerializer,
    }
    action_permissions = {
        "list": [AllowAny],
        "retrieve": [AllowAny],
    }


class OrderViewSet(ActionMixin, CustomPermissionMixin):
    queryset = Order.objects.prefetch_related("tickets")
    serializer_class = OrderSerializer

    action_serializers = {
        "list": OrderListSerializer,
        "retrieve": OrderRetrieveSerializer,
    }

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
