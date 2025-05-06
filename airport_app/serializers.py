from rest_framework import serializers

from airport_app.models import Country, City, Crew, Route, AirplaneType, Airplane, Flight, Ticket, Order, Airport


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("duration",)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
            "user"
        )
        read_only_fields = ("user",)
