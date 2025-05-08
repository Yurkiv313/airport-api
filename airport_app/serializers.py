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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class AirportSerializer(UniqueFieldsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city")

    def validate(self, data):
        self.validate_unique_fields(
            Airport, {"name": data["name"], "city": data["city"]},
            "Airport already exists."
        )
        return data


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


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
