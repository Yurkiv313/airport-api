import os
import tempfile
from PIL import Image
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from airport_app.models import Crew, Flight
from airport_app.tests.base import (
    BaseApiTestCase,
    FLIGHT_URL,
    sample_airplane,
    sample_airplane_type,
    upload_image_url,
    sample_crew,
    detail_flight_url,
    sample_route
)


class AdminAirplaneImageTests(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.authenticate_user(is_admin=True)
        self.airplane = sample_airplane(sample_airplane_type())

    def tearDown(self):
        self.airplane.image.delete()

    def test_upload_image(self):
        url = upload_image_url(self.airplane.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            res = self.client.post(url, {"image": ntf}, format="multipart")

        self.airplane.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.airplane.image)
        self.assertTrue(os.path.exists(self.airplane.image.path))

    def test_upload_invalid_image(self):
        url = upload_image_url(self.airplane.id)

        res = self.client.post(
            url, {"image": "not_an_image"}, format="multipart"
        )

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_url_is_shown_on_airplane_detail(self):
        url = upload_image_url(self.airplane.id)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")

        res = self.client.get(
            reverse(
                "airport_app:airplane-detail", args=[self.airplane.id]
            )
        )
        self.assertIn("image", res.data)

    # Flight Admin Tests
    def test_create_flight(self):
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

    def test_delete_flight(self):
        airplane_type = sample_airplane_type(name="Airtrain A500")
        flight = Flight.objects.create(
            route=sample_route(),
            airplane=sample_airplane(airplane_type),
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=2),
            is_active=True
        )
        url = detail_flight_url(flight.id)
        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_flight(self):
        airplane_type = sample_airplane_type(name="Boeing 777")
        flight = Flight.objects.create(
            route=sample_route(),
            airplane=sample_airplane(airplane_type),
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=2),
            is_active=True
        )
        main_pilot = sample_crew(position=Crew.Position.MAIN_PILOT)
        stewardess = sample_crew(
            first_name="Alica",
            last_name="White",
            position=Crew.Position.STEWARDESS
        )
        url = detail_flight_url(flight.id)
        payload = {
            "departure_time": timezone.now() + timezone.timedelta(hours=3),
            "arrival_time": timezone.now() + timezone.timedelta(hours=5),
            "crew": [main_pilot.id, stewardess.id],
        }

        res = self.client.patch(url, payload)

        flight.refresh_from_db()
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(set(flight.crew.all()), {main_pilot, stewardess})
