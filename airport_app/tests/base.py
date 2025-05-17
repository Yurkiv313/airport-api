from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport_app.models import (
    City,
    Country,
    Airport,
    Crew,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Ticket,
    Order
)

User = get_user_model()

COUNTRY_URL = reverse("airport_app:country-list")
CITY_URL = reverse("airport_app:city-list")
AIRPORT_URL = reverse("airport_app:airport-list")
CREW_URL = reverse("airport_app:crew-list")
AIRPLANE_TYPE_URL = reverse("airport_app:airplanetype-list")
AIRPLANE_URL = reverse("airport_app:airplane-list")
ROUTE_URL = reverse("airport_app:route-list")
FLIGHT_URL = reverse("airport_app:flight-list")
ORDER_URL = reverse("airport_app:order-list")


def detail_country_url(country_id):
    return reverse("airport_app:country-detail", args=[country_id])


def detail_city_url(city_id):
    return reverse("airport_app:city-detail", args=[city_id])


def detail_airport_url(airport_id):
    return reverse("airport_app:airport-detail", args=[airport_id])


def detail_crew_url(crew_id):
    return reverse("airport_app:crew-detail", args=[crew_id])


def detail_airplane_type_url(airplane_type_id):
    return reverse("airport_app:airplanetype-detail", args=[airplane_type_id])


def detail_airplane_url(airplane_id):
    return reverse("airport_app:airplane-detail", args=[airplane_id])


def upload_image_url(airplane_id):
    return reverse("airport_app:airplane-upload-image", args=[airplane_id])


def detail_route_url(route_id):
    return reverse("airport_app:route-detail", args=[route_id])


def detail_flight_url(flight_id):
    return reverse("airport_app:flight-detail", args=[flight_id])


def detail_order_url(order_id):
    return reverse("airport_app:order-detail", args=[order_id])


def sample_country(**params) -> Country:
    defaults = {"name": "Ukraine", "code": "UKR"}
    defaults.update(params)
    return Country.objects.create(**defaults)


def sample_city(country, **params) -> City:
    defaults = {"name": "Kyiv", "country": country}
    defaults.update(params)
    return City.objects.create(**defaults)


def sample_airport(city, **params) -> Airport:
    defaults = {"name": "Boryspil", "city": city}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_crew(**params) -> Crew:
    defaults = {
        "first_name": "John",
        "last_name": "Doe",
        "position": Crew.Position.MAIN_PILOT
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airplane_type(**params) -> AirplaneType:
    defaults = {"name": "Boeing 737"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(airplane_type, **params) -> Airplane:
    defaults = {
        "name": "Test Airplane",
        "rows": 30,
        "seats_in_row": 6,
        "airplane_type": airplane_type
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_route(source=None, destination=None, **params) -> Route:
    if not source:
        source = sample_airport(
            sample_city(
                sample_country(
                    name="DefaultCountry1", code="DEF"
                ),
                name="DefaultCity1"
            )
        )
    if not destination:
        destination = sample_airport(
            sample_city(
                sample_country(
                    name="DefaultCountry2", code="DF2"
                ),
                name="DefaultCity2"
            )
        )

    defaults = {"source": source, "destination": destination, "distance": 500}
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_flight(
        route=None,
        airplane_name=None,
        airplane_type_name=None
) -> Flight:
    if route is None:
        route = sample_route()

    airplane_type_name = (
            airplane_type_name or f"Airbus A320 - {timezone.now().timestamp()}"
    )
    airplane_name = airplane_name or f"Airplane - {timezone.now().timestamp()}"

    airplane_type = sample_airplane_type(name=airplane_type_name)
    airplane = (
        sample_airplane(
            airplane_type, name=airplane_name, rows=30, seats_in_row=6
        )
    )

    flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=timezone.now() + timezone.timedelta(hours=1),
        arrival_time=timezone.now() + timezone.timedelta(hours=2),
        is_active=True
    )
    pilot = sample_crew(
        first_name="John", last_name="Doe", position=Crew.Position.MAIN_PILOT
    )
    stewardess = sample_crew(
        first_name="Alice", last_name="Doe", position=Crew.Position.STEWARDESS
    )
    flight.crew.add(pilot, stewardess)

    return flight


def sample_order(user, **params) -> Order:
    defaults = {"user": user}
    defaults.update(params)
    return Order.objects.create(**defaults)


def sample_ticket(order, flight, row=1, seat=1) -> Ticket:
    return Ticket.objects.create(
        order=order, flight=flight, row=row, seat=seat
    )


class BaseApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def authenticate_user(self, is_admin=False):
        self.user = User.objects.create_user(
            email="admin@gmail.com" if is_admin else "test@gmail.com",
            password="test_password123",
            is_staff=is_admin
        )
        self.client.force_authenticate(self.user)
