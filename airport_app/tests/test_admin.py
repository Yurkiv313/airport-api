from django.utils import timezone
from rest_framework import status

from airport_app.models import Crew, Flight

from airport_app.tests.base import (
    BaseApiTestCase,
    COUNTRY_URL,
    CITY_URL,
    AIRPORT_URL,
    CREW_URL,
    AIRPLANE_TYPE_URL,
    AIRPLANE_URL,
    ROUTE_URL,
    FLIGHT_URL,
    sample_country,
    detail_country_url,
    sample_city,
    detail_city_url,
    sample_airport,
    detail_airport_url,
    sample_crew,
    detail_crew_url,
    sample_airplane_type,
    detail_airplane_type_url,
    sample_airplane,
    detail_airplane_url,
    sample_route,
    detail_route_url,
    detail_flight_url
)


class AdminTests(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.authenticate_user(is_admin=True)

    def assert_status_and_field(
            self,
            res,
            instance,
            status_code,
            field=None,
            value=None
    ):
        self.assertEquals(res.status_code, status_code)
        if field and value:
            instance.refresh_from_db()
            self.assertEquals(getattr(instance, field), value)

    def test_country_crud(self):
        payload = {"name": "Testland", "code": "TST"}
        res = self.client.post(COUNTRY_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        country = sample_country(name="Testland 1", code="T1")
        res = self.client.put(
            detail_country_url(country.id),
            {"name": "Testland Updated", "code": "T2"}
        )
        self.assert_status_and_field(
            res, country, status.HTTP_200_OK, "name", "Testland Updated"
        )

        res = self.client.patch(detail_country_url(country.id), {"code": "T3"})
        self.assert_status_and_field(
            res, country, status.HTTP_200_OK, "code", "T3"
        )

        res = self.client.delete(detail_country_url(country.id))
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_country_unique_name_and_code(self):
        sample_country(name="Testland", code="TST")
        res = self.client.post(
            COUNTRY_URL, {"name": "Testland", "code": "TST"}
        )
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

        sample_country(name="Testland 2", code="T2")
        res = self.client.post(
            COUNTRY_URL, {"name": "Testland 3", "code": "T2"}
        )
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_city_crud(self):
        country = sample_country(name="UniqueCountry1", code="UC1")
        payload = {"name": "UniqueCity1", "country": country.id}
        res = self.client.post(CITY_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        city = sample_city(country, name="UniqueCity2")
        url = detail_city_url(city.id)
        payload = {"name": "UniqueCity3"}
        res = self.client.patch(url, payload)
        self.assert_status_and_field(
            res, city, status.HTTP_200_OK, "name", "UniqueCity3"
        )

        res = self.client.patch(url, {"name": "UniqueCity4"})
        self.assert_status_and_field(
            res, city, status.HTTP_200_OK, "name", "UniqueCity4"
        )

        res = self.client.delete(detail_city_url(city.id))
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_airport_crud(self):
        country = sample_country(name="UC", code="UC")
        city = sample_city(country, name="Kyiv")

        payload = {"name": "Zhulyany", "city": city.id}
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        airport = sample_airport(city, name="Zhulyany")

        payload = {"name": "New Zhulyany"}
        res = self.client.patch(detail_airport_url(airport.id), payload)
        self.assert_status_and_field(
            res, airport, status.HTTP_200_OK, "name", "New Zhulyany"
        )

        res = self.client.patch(
            detail_airport_url(airport.id), {"name": "Boryspil"}
        )
        self.assert_status_and_field(
            res, airport, status.HTTP_200_OK, "name", "Boryspil"
        )

        res = self.client.delete(detail_airport_url(airport.id))
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_airport_with_existing_name_and_city(self):
        country = sample_country()
        city = sample_city(country)
        sample_airport(city, name="Boryspil")

        payload = {"name": "Boryspil", "city": city.id}
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_airport_with_different_city(self):
        country = sample_country()
        city1 = sample_city(country, name="Kyiv")
        city2 = sample_city(country, name="Lviv")

        sample_airport(city1, name="Boryspil")

        payload = {"name": "Boryspil", "city": city2.id}
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_crew_crud(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "position": Crew.Position.STEWARDESS,
        }

        res = self.client.post(CREW_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        crew = sample_crew(
            first_name="Jane",
            last_name="Smith",
            position=Crew.Position.STEWARDESS
        )

        payload = {"first_name": "Michael"}
        res = self.client.patch(detail_crew_url(crew.id), payload)
        self.assert_status_and_field(
            res, crew, status.HTTP_200_OK, "first_name", "Michael"
        )

        res = self.client.patch(
            detail_crew_url(crew.id), {"last_name": "Johnson"}
        )
        self.assert_status_and_field(
            res, crew, status.HTTP_200_OK, "last_name", "Johnson"
        )

        res = self.client.delete(detail_crew_url(crew.id))
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_position(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "position": "XX",
        }

        res = self.client.post(CREW_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_airplane_type_crud(self):
        unique_name = "Airbus A320 Unique"
        payload = {
            "name": unique_name,
        }
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        airplane_type = sample_airplane_type(name="Airbus A420 Unique")

        new_name = "Airbus A380 Unique"
        payload = {"name": new_name}
        res = self.client.patch(
            detail_airplane_type_url(airplane_type.id), payload
        )
        self.assert_status_and_field(
            res, airplane_type, status.HTTP_200_OK, "name", new_name
        )

        another_name = "Boeing 737 Unique"
        res = self.client.patch(
            detail_airplane_type_url(airplane_type.id), {"name": another_name}
        )
        self.assert_status_and_field(
            res, airplane_type, status.HTTP_200_OK, "name", another_name
        )

        res = self.client.delete(detail_airplane_type_url(airplane_type.id))
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_airplane_type_with_existing_name(self):
        unique_name = "Boeing 737 Unique"
        sample_airplane_type(name=unique_name)

        payload = {"name": unique_name}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_airplane_crud(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Test Airplane",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        airplane = sample_airplane(airplane_type)
        payload = {"name": "Updated Airplane"}
        url = detail_airplane_url(airplane.id)
        res = self.client.patch(url, payload)
        airplane.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(airplane.name, "Updated Airplane")

        res = self.client.patch(url, {"name": "Partially Updated Airplane"})
        airplane.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(airplane.name, "Partially Updated Airplane")

        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_airplane_with_existing_name_and_type(self):
        airplane_type = sample_airplane_type()
        sample_airplane(airplane_type, name="Test Airplane")
        payload = {
            "name": "Test Airplane",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_route_crud(self):
        country = sample_country()
        city_source = sample_city(country, name="Kyiv")
        city_destination = sample_city(country, name="Lviv")
        airport_source = sample_airport(city_source, name="Boryspil Airport")
        airport_destination = sample_airport(
            city_destination, name="Lviv Airport"
        )
        payload = {
            "source": airport_source.id,
            "destination": airport_destination.id,
            "distance": 500
        }
        res = self.client.post(ROUTE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        route = sample_route(
            source=airport_source, destination=airport_destination
        )
        new_airport = sample_airport(
            city=sample_city(country, name="Kharkiv"), name="Kharkiv Airport"
        )
        url = detail_route_url(route.id)
        payload = {
            "source": route.source.id,
            "destination": new_airport.id,
            "distance": 700
        }
        res = self.client.put(url, payload)
        route.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(route.destination, new_airport)

        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_route_with_same_source_and_destination(self):
        airport = sample_airport(sample_city(sample_country(), name="Dnipro"))
        payload = {
            "source": airport.id,
            "destination": airport.id,
            "distance": 300
        }
        res = self.client.post(ROUTE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_route_with_zero_distance(self):
        route = sample_route()
        url = detail_route_url(route.id)
        payload = {
            "source": route.source.id,
            "destination": route.destination.id,
            "distance": 0
        }
        res = self.client.put(url, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Flight Tests
    def test_flight_crud(self):
        route = sample_route()
        airplane_type = sample_airplane_type(name="Airbus A320")
        airplane = sample_airplane(airplane_type)
        main_pilot = sample_crew(position=Crew.Position.MAIN_PILOT)
        stewardess = sample_crew(
            first_name="Alica",
            last_name="Black",
            position=Crew.Position.STEWARDESS
        )

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": timezone.now(),
            "arrival_time": timezone.now() + timezone.timedelta(hours=2),
            "crew": [main_pilot.id, stewardess.id],
            "is_active": True
        }
        res = self.client.post(FLIGHT_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        flight = Flight.objects.get(id=res.data["id"])
        new_pilot = sample_crew(position=Crew.Position.MAIN_PILOT)
        payload = {
            "departure_time": timezone.now() + timezone.timedelta(hours=3),
            "arrival_time": timezone.now() + timezone.timedelta(hours=5),
            "crew": [new_pilot.id, stewardess.id],
        }
        url = detail_flight_url(flight.id)
        res = self.client.patch(url, payload)
        flight.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(set(flight.crew.all()), {new_pilot, stewardess})

        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
