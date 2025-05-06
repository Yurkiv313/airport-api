from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name} - {self.country.code}"


class Crew(models.Model):
    class Position(models.TextChoices):
        MAIN_PILOT = "MP", "Main Pilot"
        SECOND_PILOT = "SP", "Second Pilot"
        STEWARDESS = "ST", "Stewardess"
        MEDIC = "MD", "Medic"
        CREW_MEMBER = "CM", "Crew Member"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(
        max_length=2,
        choices=Position,
        default=Position.CREW_MEMBER,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} - {self.position}"


class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="airports")

    def __str__(self):
        return f"{self.name} ({self.city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_to")
    distance = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"Source: {self.source} "
            f"Destination {self.destination} "
            f"Distance: {self.distance}"
        )


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    @property
    def is_large(self):
        return self.capacity > 200

    def __str__(self):
        return f"{self.name} ({self.airplane_type.name})"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField("Crew", related_name="flights")
    is_active = models.BooleanField(default=True)

    @property
    def duration(self):
        return self.arrival_time - self.departure_time

    def __str__(self):
        return f"{self.route} at {self.departure_time.strftime('%Y-%m-%d %H:%M')}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order by {self.user} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "flight"],
                name="unique_seat_per_flight"
            )
        ]

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for value, name, limit_attr in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row")
        ]:
            limit = getattr(airplane, limit_attr)
            if not 1 <= value <= limit:
                raise error_to_raise(
                    f"{name} must be in range 1:{limit}"
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
