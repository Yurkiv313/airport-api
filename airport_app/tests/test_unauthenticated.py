from rest_framework import status
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
    ORDER_URL
)


class UnauthenticatedTests(BaseApiTestCase):

    def test_auth_required(self):
        urls = [
            (COUNTRY_URL, status.HTTP_401_UNAUTHORIZED),
            (CITY_URL, status.HTTP_401_UNAUTHORIZED),
            (AIRPORT_URL, status.HTTP_401_UNAUTHORIZED),
            (CREW_URL, status.HTTP_401_UNAUTHORIZED),
            (AIRPLANE_TYPE_URL, status.HTTP_401_UNAUTHORIZED),
            (AIRPLANE_URL, status.HTTP_401_UNAUTHORIZED),
            (ROUTE_URL, status.HTTP_401_UNAUTHORIZED),
            (FLIGHT_URL, status.HTTP_200_OK),
            (ORDER_URL, status.HTTP_401_UNAUTHORIZED),
        ]

        for url, expected_status in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, expected_status)
