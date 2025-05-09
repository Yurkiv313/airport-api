from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError as DRFValidationError
from airport_app.models import Country, City, Crew, Route, AirplaneType, Airplane, Flight, Ticket, Order, Airport


class UniqueFieldsValidatorMixin:
    def validate_unique_fields(self, model, unique_fields: dict, message: str):
        if model.objects.filter(**unique_fields).exists():
            raise serializers.ValidationError(message)


class CountrySerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code")

    def validate(self, data):
        self.validate_unique_fields(
            Country, {"name": data["name"]},
            "Country with this name or code already exists."
        )
        self.validate_unique_fields(
            Country, {"code": data["code"]},
            "Country with this code already exists."
        )
        return data


class CountryListSerializer(CountrySerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")

    def validate(self, data):
        self.validate_unique_fields(
            City, {"name": data["name"], "country": data["country"]},
            "City already exists."
        )
        return data


class CityListSerializer(CitySerializer):
    country = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class CityRetrieveSerializer(CitySerializer):
    country = CountrySerializer()


class CrewSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name", "position")

    def get_position(self, obj):
        return obj.get_position_display()


class CrewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name", "position")


class AirportSerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    city = CityRetrieveSerializer()

    class Meta:
        model = Airport
        fields = ("id", "name", "city")

    def validate(self, data):
        self.validate_unique_fields(
            Airport, {"name": data["name"], "city": data["city"]},
            "Airport already exists."
        )
        return data


class AirportListSerializer(AirportSerializer):
    city = serializers.CharField(
        source="city.name", read_only=True
    )
    country_code = serializers.CharField(
        source="city.country.code", read_only=True
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "city", "country_code")


class RouteSerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, data):
        if data["source"] == data["destination"]:
            raise serializers.ValidationError("Source and destination airports must be different.")
        elif data["distance"] <= 0:
            raise serializers.ValidationError("Distance must be greater than 0 kilometers.")
        self.validate_unique_fields(
            Route, {"source": data["source"], "destination": data["destination"]},
            "Route already exists."
        )
        return data


class RouteListSerializer(RouteSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportListSerializer()
    destination = AirportListSerializer()


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "is_large",
            "airplane_type"
        )
        read_only_fields = ("capacity", "is_large")

    def validate(self, data):
        self.validate_unique_fields(
            Airplane, {"name": data["name"], "airplane_type": data["airplane_type"]},
            "Airplane already exists."
        )
        return data


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        source="airplane_type.name", read_only=True
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "is_large",
            "airplane_type"
        )
        read_only_fields = ("capacity", "is_large")


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "duration",
            "is_active"
        )
        read_only_fields = ("duration", "is_active")

    def validate(self, attrs):
        departure = attrs.get("departure_time")
        arrival = attrs.get("arrival_time")
        airplane = attrs.get("airplane")

        if arrival <= departure:
            raise serializers.ValidationError("Arrival time must be later than the departure time.")

        crew = attrs.get("crew")
        if not crew:
            raise serializers.ValidationError("Crew is required.")

        main_pilots = [member for member in crew if member.position == Crew.Position.MAIN_PILOT]
        stewardesses = [member for member in crew if member.position == Crew.Position.STEWARDESS]

        if not main_pilots:
            raise serializers.ValidationError("The crew must include at least one main pilot.")

        if not stewardesses:
            raise serializers.ValidationError("The crew must include at least one stewardess.")

        current_id = self.instance.id if self.instance else None

        def check_overlapping_flights(obj, obj_type):
            overlapping_flights = obj.flights.filter(
                departure_time__lt=arrival,
                arrival_time__gt=departure,
            ).exclude(id=current_id)

            if overlapping_flights.exists():
                raise serializers.ValidationError(
                    f"{obj_type} {obj} is already scheduled for another flight during this time."
                )

        for crew_member in crew:
            check_overlapping_flights(crew_member, "Crew member")

        if airplane:
            check_overlapping_flights(airplane, "Airplane")

        return attrs


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    airplane = serializers.CharField(source="airplane.name", read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "duration",
            "is_active"
        )
        read_only_fields = ("duration", "is_active")

    def get_route(self, obj):
        return {
            "source": obj.route.source.name,
            "destination": obj.route.destination.name,
            "distance": f"{obj.route.distance} km"
        }


class FlightRetrieveSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    airplane = AirplaneRetrieveSerializer()
    crew = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "duration",
            "crew",
            "is_active"
        )
        read_only_fields = ("duration", "is_active")

    def get_route(self, obj):
        return {
            "source": {
                "name": obj.route.source.name,
                "city": obj.route.source.city.name,
                "country": obj.route.source.city.country.name
            },
            "destination": {
                "name": obj.route.destination.name,
                "city": obj.route.destination.city.name,
                "country": obj.route.destination.city.country.name
            },
            "distance": f"{obj.route.distance} km"
        }

    def get_crew(self, obj):
        return [
            {
                "full_name": member.full_name,
                "position": member.get_position_display()
            }
            for member in obj.crew.all()
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )

    def validate(self, attrs):
        data = super().validate(attrs)

        row = attrs.get("row")
        seat = attrs.get("seat")
        flight = attrs.get("flight")

        if row is None or seat is None or flight is None:
            raise serializers.ValidationError("Row, seat, and flight are required.")

        airplane = flight.airplane
        Ticket.validate_ticket(
            row,
            seat,
            airplane,
            DRFValidationError
        )

        return data


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
            "user"
        )
        read_only_fields = ("user",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets", "user")

    def get_tickets(self, obj):
        return [
            {
                "row": ticket.row,
                "seat": ticket.seat,
                "from": ticket.flight.route.source.city.country.name,
                "to": ticket.flight.route.destination.city.country.name
            }
            for ticket in obj.tickets.all()
        ]


class OrderRetrieveSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")

    def get_tickets(self, obj):
        return [
            {
                "row": ticket.row,
                "seat": ticket.seat,
                "route": {
                    "from": ticket.flight.route.source.city.country.name,
                    "to": ticket.flight.route.destination.city.country.name,
                    "source": ticket.flight.route.source.name,
                    "destination": ticket.flight.route.destination.name,
                    "distance": f"{ticket.flight.route.distance} km"
                },
                "flight": {
                    "departure_time": ticket.flight.departure_time,
                    "arrival_time": ticket.flight.arrival_time,
                    "duration": ticket.flight.duration,
                    "airplane": ticket.flight.airplane.name
                }
            }
            for ticket in obj.tickets.all()
        ]
