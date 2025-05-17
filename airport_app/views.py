from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
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
    AirportRetrieveSerializer,
    AirplaneImageSerializer,
)
from airport_app.utils.mixins import ActionMixin, CustomPermissionMixin
from airport_app.utils.schema_descriptions import (
    country_list_schema,
    country_retrieve_schema,
    country_create_schema,
    country_update_schema,
    country_destroy_schema,
    city_list_schema,
    city_retrieve_schema,
    city_create_schema,
    city_update_schema,
    city_destroy_schema,
    crew_list_schema,
    crew_retrieve_schema,
    crew_create_schema,
    crew_update_schema,
    crew_destroy_schema,
    airport_list_schema,
    airport_retrieve_schema,
    airport_create_schema,
    airport_update_schema,
    airport_destroy_schema,
    route_list_schema,
    route_retrieve_schema,
    route_create_schema,
    route_update_schema,
    route_destroy_schema,
    airplane_type_list_schema,
    airplane_type_retrieve_schema,
    airplane_type_create_schema,
    airplane_type_update_schema,
    airplane_type_destroy_schema,
    airplane_list_schema,
    airplane_retrieve_schema,
    airplane_create_schema,
    airplane_update_schema,
    airplane_destroy_schema,
    airplane_upload_image_schema,
    flight_list_schema,
    flight_retrieve_schema,
    flight_create_schema,
    flight_update_schema,
    flight_destroy_schema,
    order_list_schema,
    order_retrieve_schema,
    order_create_schema,
    order_update_schema,
    order_destroy_schema
)


class CountryViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage countries in the system. Admins can create/update/delete.
    Authenticated users can view the list and detail.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    action_serializers = {"list": CountryListSerializer}

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
    }

    @country_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @country_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @country_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @country_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @country_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CityViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage cities in the system. Admins can create/update/delete.
    Authenticated users can view list of cities and details.
    """

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

    @city_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @city_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @city_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @city_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @city_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CrewViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage crew members (pilots, stewardesses, etc.) Admins only.
    """

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

    @crew_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @crew_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @crew_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @crew_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @crew_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AirportViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage airports. Authenticated users can view the list and detail.
    """

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

    @airport_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @airport_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @airport_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @airport_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @airport_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RouteViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage flight routes between airports. Admins can create/update/delete.
    Authenticated users can view list and details.
    """

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

    @route_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AirplaneTypeViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage airplane types (e.g. Boeing 737, Airbus A320).
    Admins only.
    """

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    action_permissions = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
    }

    @airplane_type_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @airplane_type_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @airplane_type_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @airplane_type_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @airplane_type_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AirplaneViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage airplanes. Admins only.
    """

    queryset = Airplane.objects.select_related("airplane_type").order_by("id")
    serializer_class = AirplaneSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["airplane_type"]
    search_fields = ["name"]

    action_serializers = {
        "list": AirplaneListSerializer,
        "retrieve": AirplaneRetrieveSerializer,
        "upload_image": AirplaneImageSerializer,
    }

    action_permissions = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
    }

    @airplane_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @airplane_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @airplane_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @airplane_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @airplane_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @airplane_upload_image_schema
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class FlightViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage flights and their scheduling.
    Public access to list and detail.
    Admins only for creation and updates.
    """

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

    @flight_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @flight_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @flight_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @flight_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @flight_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage flight ticket orders.
    Authenticated users can view and create their orders.
    """

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

    @order_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @order_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @order_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @order_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @order_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
