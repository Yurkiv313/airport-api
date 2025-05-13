from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
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

    @extend_schema(
        summary="Get list of countries",
        description="Return a list of countries. Supports search by name.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search countries by name (case-insensitive)"
                            " Examples: Ukraine, Ger",
            ),
        ],
        responses={200: CountryListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a country",
        description="Get detailed information about a specific country by ID.",
        responses={200: CountrySerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a country",
        description="Admins only. Create a new country with a unique name and code.",
        responses={201: CountrySerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a country",
        description="Admins only. Update the name or code of an existing country.",
        responses={200: CountrySerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a country",
        description="Admins only. Delete a country by ID.",
        responses={204: None},
    )
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

    @extend_schema(
        summary="Get list of cities",
        description=(
                "Return a list of cities.\n\n"
                "- Supports search by name (case-insensitive)\n"
                "- Filter by country ID (`country=1`)"
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search cities by name. Examples: Lviv, Par",
            ),
            OpenApiParameter(
                name="country",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter cities by country ID. Example: 1",
            ),
        ],
        responses={200: CityListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a city",
        description="Get detailed information about a specific city by ID.",
        responses={200: CityRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a city",
        description="Admins only. Create a new city with a unique name in a specific country.",
        responses={201: CitySerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a city",
        description="Admins only. Update the name or country of an existing city.",
        responses={200: CitySerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a city",
        description="Admins only. Delete a city by ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CrewViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage crew members (pilots, stewardesses, etc). Admins only.
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

    @extend_schema(
        summary="Get list of crew members",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a crew member",
        description="Get full details of a crew member by ID (admin only).",
        responses={200: CrewRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a crew member",
        description="Admins only. Add a new crew member with a name and position.",
        responses={201: CrewSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a crew member",
        description="Admins only. Update crew member details.",
        responses={200: CrewSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a crew member",
        description="Admins only. Remove a crew member by ID.",
        responses={204: None},
    )
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

    @extend_schema(
        summary="Get list of airports",
        description=(
                "Return a list of airports.\n\n"
                "- Search by name\n"
                "- Filter by city ID (`city=3`)\n"
                "- Filter by country ID of city (`city__country=2`)"
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search airports by name. Example: Heathrow",
            ),
            OpenApiParameter(
                name="city",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by city ID. Example: 3",
            ),
            OpenApiParameter(
                name="city__country",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by country ID (via city). Example: 2",
            ),
        ],
        responses={200: AirportListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an airport",
        description="Get detailed information about an airport by ID.",
        responses={200: AirportRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create an airport",
        description="Admins only. Create a new airport with name and city.",
        responses={201: AirportSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an airport",
        description="Admins only. Update airport name or change city.",
        responses={200: AirportSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an airport",
        description="Admins only. Delete an airport by ID.",
        responses={204: None},
    )
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

    @extend_schema(
        summary="Get list of routes",
        description=(
                "Return a list of flight routes between airports.\n\n"
                "- Filter by source airport ID (`source=1`)\n"
                "- Filter by destination airport ID (`destination=2`)\n"
                "- Search by source or destination airport name"
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by airport names. Example: Boryspil",
            ),
            OpenApiParameter(
                name="source",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by source airport ID. Example: 1",
            ),
            OpenApiParameter(
                name="destination",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by destination airport ID. Example: 2",
            ),
        ],
        responses={200: RouteListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a route",
        description="Get detailed information about a flight route by ID.",
        responses={200: RouteRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a route",
        description=(
                "Admins only. Create a new flight route.\n"
                "- Source and destination must be different\n"
                "- Distance must be greater than 0"
        ),
        responses={201: RouteSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a route",
        description="Admins only. Update the route information.",
        responses={200: RouteSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a route",
        description="Admins only. Delete a flight route by ID.",
        responses={204: None},
    )
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

    @extend_schema(
        summary="Get list of airplane types",
        description="Admins only. Return a list of available airplane types.",
        responses={200: AirplaneTypeSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an airplane type",
        description="Admins only. Get detailed info about an airplane type by ID.",
        responses={200: AirplaneTypeSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create an airplane type",
        description="Admins only. Create a new airplane type.",
        responses={201: AirplaneTypeSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an airplane type",
        description="Admins only. Update an airplane type's name.",
        responses={200: AirplaneTypeSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an airplane type",
        description="Admins only. Delete an airplane type by ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AirplaneViewSet(ActionMixin, CustomPermissionMixin):
    """
    Manage airplanes. Admins only.
    """
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

    @extend_schema(
        summary="Get list of airplanes",
        description="Admins only. Return a list of airplanes. Filter by airplane type, search by name.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by airplane name. Example: Airbus A320"
            ),
            OpenApiParameter(
                name="airplane_type",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by airplane type ID. Example: 1"
            ),
        ],
        responses={200: AirplaneListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an airplane",
        description="Admins only. Get full details about an airplane.",
        responses={200: AirplaneRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create an airplane",
        description="Admins only. Create a new airplane with its specifications.",
        responses={201: AirplaneSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an airplane",
        description="Admins only. Update airplane details.",
        responses={200: AirplaneSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an airplane",
        description="Admins only. Delete an airplane by ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Upload airplane image",
        description="Admins only. Upload an image for the selected airplane.",
        request=AirplaneImageSerializer,
        responses={200: AirplaneImageSerializer},
    )
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

    @extend_schema(
        summary="Get list of flights",
        description=(
                "Return a list of scheduled flights.\n\n"
                "- Search by source/destination airport names\n"
                "- Filter by route ID, airplane ID, active status, or date range"
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by airport name. Example: Heathrow"
            ),
            OpenApiParameter(
                name="route",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by route ID"
            ),
            OpenApiParameter(
                name="airplane",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by airplane ID"
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter by active status"
            ),
            OpenApiParameter(
                name="departure_time",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Filter flights that depart after this time"
            ),
            OpenApiParameter(
                name="arrival_time",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Filter flights that arrive before this time"
            ),
        ],
        responses={200: FlightListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a flight",
        description="Get full details about a specific flight.",
        responses={200: FlightRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a flight",
        description=(
                "Admins only. Create a flight with:\n"
                "- A valid route and airplane\n"
                "- A crew that includes at least one main pilot and one stewardess\n"
                "- Departure time must be before arrival time\n"
                "- No overlapping flights for airplane or crew"
        ),
        responses={201: FlightSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a flight",
        description="Admins only. Update flight information and validate constraints.",
        responses={200: FlightSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a flight",
        description="Admins only. Delete a flight by ID.",
        responses={204: None},
    )
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

    @extend_schema(
        summary="Get list of orders",
        description="Return all orders for the authenticated user. Admins see all orders.",
        responses={200: OrderListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an order",
        description="Return details of a specific order belonging to the authenticated user.",
        responses={200: OrderRetrieveSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create an order",
        description=(
                "Create a new flight ticket order.\n"
                "- The user is set automatically from the request.\n"
                "- You must provide at least one ticket with `row`, `seat`, and `flight`.\n"
                "- Validation will check if the seats are available."
        ),
        request=OrderSerializer,
        responses={201: OrderSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an order",
        description="Admins only. Update an order and its tickets (not commonly used).",
        responses={200: OrderSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an order",
        description="Admins only. Delete an order by ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
