from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from airport_app.serializers import (
    CountryListSerializer,
    CountrySerializer,
    CityListSerializer,
    CityRetrieveSerializer,
    CitySerializer,
    CrewRetrieveSerializer,
    CrewSerializer,
    AirportListSerializer,
    AirportRetrieveSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    AirplaneSerializer,
    AirplaneImageSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    FlightSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    OrderSerializer
)

country_list_schema = extend_schema(
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

country_retrieve_schema = extend_schema(
        summary="Retrieve a country",
        description="Get detailed information about a specific country by ID.",
        responses={200: CountrySerializer},
    )

country_create_schema = extend_schema(
        summary="Create a country",
        description="Admins only. "
        "Create a new country with a unique name and code.",
        responses={201: CountrySerializer},
    )

country_update_schema = extend_schema(
        summary="Update a country",
        description="Admins only. "
        "Update the name or code of an existing country.",
        responses={200: CountrySerializer},
    )

country_destroy_schema = extend_schema(
        summary="Delete a country",
        description="Admins only. Delete a country by ID.",
        responses={204: None},
    )

city_list_schema = extend_schema(
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

city_retrieve_schema = extend_schema(
        summary="Retrieve a city",
        description="Get detailed information about a specific city by ID.",
        responses={200: CityRetrieveSerializer},
    )

city_create_schema = extend_schema(
        summary="Create a city",
        description="Admins only. "
        "Create a new city with a unique name "
        "in a specific country.",
        responses={201: CitySerializer},
    )


city_update_schema = extend_schema(
        summary="Update a city",
        description="Admins only. "
        "Update the name or country of an existing city.",
        responses={200: CitySerializer},
    )


city_destroy_schema = extend_schema(
        summary="Delete a city",
        description="Admins only. Delete a city by ID.",
        responses={204: None},
    )


crew_list_schema = extend_schema(
        summary="Get list of crew members",
    )

crew_retrieve_schema = extend_schema(
        summary="Retrieve a crew member",
        description="Get full details of a crew member by ID (admin only).",
        responses={200: CrewRetrieveSerializer},
    )

crew_create_schema = extend_schema(
        summary="Create a crew member",
        description="Admins only. "
        "Add a new crew member with a name and position.",
        responses={201: CrewSerializer},
    )


crew_update_schema = extend_schema(
        summary="Update a crew member",
        description="Admins only. Update crew member details.",
        responses={200: CrewSerializer},
    )


crew_destroy_schema = extend_schema(
        summary="Delete a crew member",
        description="Admins only. Remove a crew member by ID.",
        responses={204: None},
    )


airport_list_schema = extend_schema(
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

airport_retrieve_schema = extend_schema(
        summary="Retrieve an airport",
        description="Get detailed information about an airport by ID.",
        responses={200: AirportRetrieveSerializer},
    )


airport_create_schema = extend_schema(
        summary="Create an airport",
        description="Admins only. Create a new airport with name and city.",
        responses={201: AirportSerializer},
    )

airport_update_schema = extend_schema(
        summary="Update an airport",
        description="Admins only. Update airport name or change city.",
        responses={200: AirportSerializer},
    )

airport_destroy_schema = extend_schema(
        summary="Delete an airport",
        description="Admins only. Delete an airport by ID.",
        responses={204: None},
    )

route_list_schema = extend_schema(
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

route_retrieve_schema = extend_schema(
        summary="Retrieve a route",
        description="Get detailed information about a flight route by ID.",
        responses={200: RouteRetrieveSerializer},
    )

route_create_schema = extend_schema(
        summary="Create a route",
        description=(
            "Admins only. Create a new flight route.\n"
            "- Source and destination must be different\n"
            "- Distance must be greater than 0"
        ),
        responses={201: RouteSerializer},
    )


route_update_schema = extend_schema(
        summary="Update a route",
        description="Admins only. Update the route information.",
        responses={200: RouteSerializer},
    )


route_destroy_schema = extend_schema(
        summary="Delete a route",
        description="Admins only. Delete a flight route by ID.",
        responses={204: None},
    )

airplane_type_list_schema = extend_schema(
        summary="Get list of airplane types",
        description="Admins only. Return a list of available airplane types.",
        responses={200: AirplaneTypeSerializer(many=True)},
    )

airplane_type_retrieve_schema = extend_schema(
        summary="Retrieve an airplane type",
        description="Admins only. "
        "Get detailed info about an airplane type by ID.",
        responses={200: AirplaneTypeSerializer},
    )


airplane_type_create_schema = extend_schema(
        summary="Create an airplane type",
        description="Admins only. Create a new airplane type.",
        responses={201: AirplaneTypeSerializer},
    )

airplane_type_update_schema = extend_schema(
        summary="Update an airplane type",
        description="Admins only. Update an airplane type's name.",
        responses={200: AirplaneTypeSerializer},
    )


airplane_type_destroy_schema = extend_schema(
        summary="Delete an airplane type",
        description="Admins only. Delete an airplane type by ID.",
        responses={204: None},
    )


airplane_list_schema = extend_schema(
        summary="Get list of airplanes",
        description="Admins only. "
        "Return a list of airplanes. "
        "Filter by airplane type, search by name.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by airplane name. Example: Airbus A320",
            ),
            OpenApiParameter(
                name="airplane_type",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by airplane type ID. Example: 1",
            ),
        ],
        responses={200: AirplaneListSerializer(many=True)},
    )


airplane_retrieve_schema = extend_schema(
        summary="Retrieve an airplane",
        description="Admins only. Get full details about an airplane.",
        responses={200: AirplaneRetrieveSerializer},
    )

airplane_create_schema = extend_schema(
        summary="Create an airplane",
        description="Admins only. "
        "Create a new airplane with its specifications.",
        responses={201: AirplaneSerializer},
    )


airplane_update_schema = extend_schema(
        summary="Update an airplane",
        description="Admins only. Update airplane details.",
        responses={200: AirplaneSerializer},
    )


airplane_destroy_schema = extend_schema(
        summary="Delete an airplane",
        description="Admins only. Delete an airplane by ID.",
        responses={204: None},
    )

airplane_upload_image_schema = extend_schema(
        summary="Upload airplane image",
        description="Admins only. Upload an image for the selected airplane.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "image": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        },
        responses={200: AirplaneImageSerializer},
    )

flight_list_schema = extend_schema(
        summary="Get list of flights",
        description=(
            "Return a list of scheduled flights.\n\n"
            "- Search by source/destination airport names\n"
            "- Filter by route ID, "
            "airplane ID, active status, or date range"
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by airport name. Example: Heathrow",
            ),
            OpenApiParameter(
                name="route",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by route ID",
            ),
            OpenApiParameter(
                name="airplane",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by airplane ID",
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter by active status",
            ),
            OpenApiParameter(
                name="departure_time",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Filter flights that depart after this time",
            ),
            OpenApiParameter(
                name="arrival_time",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Filter flights that arrive before this time",
            ),
        ],
        responses={200: FlightListSerializer(many=True)},
    )


flight_retrieve_schema = extend_schema(
        summary="Retrieve a flight",
        description="Get full details about a specific flight.",
        responses={200: FlightRetrieveSerializer},
    )


flight_create_schema = extend_schema(
        summary="Create a flight",
        description=(
            "Admins only. Create a flight with:\n"
            "- A valid route and airplane\n"
            "- A crew that includes at least "
            "one main pilot and one stewardess\n"
            "- Departure time must be before arrival time\n"
            "- No overlapping flights for airplane or crew"
        ),
        responses={201: FlightSerializer},
    )


flight_update_schema = extend_schema(
        summary="Update a flight",
        description="Admins only. "
        "Update flight information and validate constraints.",
        responses={200: FlightSerializer},
    )

flight_destroy_schema = extend_schema(
        summary="Delete a flight",
        description="Admins only. Delete a flight by ID.",
        responses={204: None},
    )

order_list_schema = extend_schema(
        summary="Get list of orders",
        description="Return all orders for the authenticated user. "
        "Admins see all orders.",
        responses={200: OrderListSerializer(many=True)},
    )

order_retrieve_schema = extend_schema(
        summary="Retrieve an order",
        description="Return details of a specific order"
        " belonging to the authenticated user.",
        responses={200: OrderRetrieveSerializer},
    )


order_create_schema = extend_schema(
        summary="Create an order",
        description=(
            "Create a new flight ticket order.\n"
            "- The user is set automatically from the request.\n"
            "- You must provide at least one ticket"
            " with `row`, `seat`, and `flight`.\n"
            "- Validation will check if the seats are available."
        ),
        request=OrderSerializer,
        responses={201: OrderSerializer},
    )

order_update_schema = extend_schema(
        summary="Update an order",
        description="Admins only. "
        "Update an order and its tickets (not commonly used).",
        responses={200: OrderSerializer},
    )

order_destroy_schema = extend_schema(
        summary="Delete an order",
        description="Admins only. Delete an order by ID.",
        responses={204: None},
    )
