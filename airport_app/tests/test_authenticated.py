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
    ORDER_URL,
    detail_country_url,
    detail_city_url,
    detail_airport_url,
    detail_crew_url,
    detail_airplane_type_url,
    detail_airplane_url,
    detail_route_url,
    detail_flight_url,
    sample_country,
    sample_city,
    sample_airport,
    sample_crew,
    sample_airplane_type,
    sample_airplane,
    sample_route,
    sample_flight,
    sample_order,
    detail_order_url
)

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    Flight,
    Order,
    Ticket
)

from airport_app.serializers import (
    CountryListSerializer,
    CountrySerializer,
    CityListSerializer,
    CityRetrieveSerializer,
    AirportListSerializer,
    AirportRetrieveSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderListSerializer,
)


class AuthenticatedTests(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.authenticate_user()

    def test_model_str_methods(self):
        country = sample_country(name="Test Country", code="TC")
        city = sample_city(country, name="Test City")
        airport = sample_airport(city, name="Test Airport")
        crew = sample_crew(first_name="John", last_name="Doe")
        airplane_type = sample_airplane_type(name="Test Airplane Type")
        airplane = sample_airplane(airplane_type, name="Test Airplane")
        route = sample_route(
            source=airport,
            destination=sample_airport(
                city,
                name="Test Destination"
            )
        )
        flight = sample_flight()

        self.assertEqual(str(country), "Test Country")
        self.assertEqual(str(city), "Test City - TC")
        self.assertEqual(str(airport), "Test Airport (Test City - TC)")
        self.assertEqual(str(crew), "John - MP")
        self.assertEqual(str(airplane_type), "Test Airplane Type")
        self.assertEqual(
            str(airplane), f"{airplane.name} ({airplane_type.name})"
        )
        self.assertEqual(
            str(route),
            f"Source: {route.source} "
            f"Destination {route.destination} "
            f"Distance: {route.distance}"
        )
        self.assertEqual(
            str(flight),
            f"{flight.route} at "
            f"{flight.departure_time.strftime('%Y-%m-%d %H:%M')}"
        )

    def test_country_list_and_detail(self):
        sample_country(name="Testland", code="TST")
        sample_country(name="Poland", code="PLN")

        res_list = self.client.get(COUNTRY_URL)
        countries = Country.objects.all()
        serializer_list = CountryListSerializer(countries, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

        country = sample_country(name="France", code="FRA")
        res_detail = self.client.get(detail_country_url(country.id))
        serializer_detail = CountrySerializer(country)

        self.assertEquals(res_detail.status_code, status.HTTP_200_OK)
        self.assertEquals(res_detail.data, serializer_detail.data)

    def test_city_list_and_detail(self):
        country = sample_country(name="Testland", code="TST")
        sample_city(country, name="City1")
        city = sample_city(country, name="City2")

        res_list = self.client.get(CITY_URL)
        cities = City.objects.all()
        serializer_list = CityListSerializer(cities, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

        res_detail = self.client.get(detail_city_url(city.id))
        serializer_detail = CityRetrieveSerializer(city)

        self.assertEquals(res_detail.status_code, status.HTTP_200_OK)
        self.assertEquals(res_detail.data, serializer_detail.data)

    def test_airport_list_and_detail(self):
        country = sample_country(name="Testland", code="TST")
        city = sample_city(country, name="City1")
        sample_airport(city, name="Airport1")
        airport = sample_airport(city, name="Airport2")

        res_list = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer_list = AirportListSerializer(airports, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

        res_detail = self.client.get(detail_airport_url(airport.id))
        serializer_detail = AirportRetrieveSerializer(airport)

        self.assertEquals(res_detail.status_code, status.HTTP_200_OK)
        self.assertEquals(res_detail.data, serializer_detail.data)

    def test_forbidden_crew_list_access(self):
        res = self.client.get(CREW_URL)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_retrieve_crew_access(self):
        crew = sample_crew()
        url = detail_crew_url(crew.id)
        res = self.client.get(url)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_airplane_type_list_access(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_retrieve_airplane_type_access(self):
        airplane_type = sample_airplane_type()
        url = detail_airplane_type_url(airplane_type.id)
        res = self.client.get(url)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_airplane_list_access(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_retrieve_airplane_access(self):
        airplane = sample_airplane(sample_airplane_type())
        url = detail_airplane_url(airplane.id)
        res = self.client.get(url)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_list_and_detail(self):
        country1 = sample_country(name="Testland", code="TST")
        country2 = sample_country(name="Poland", code="PLN")
        city1 = sample_city(country1, name="City1")
        city2 = sample_city(country2, name="City2")
        airport1 = sample_airport(city1, name="Airport1")
        airport2 = sample_airport(city2, name="Airport2")

        route1 = sample_route(
            source=airport1, destination=airport2, distance=500
        )
        route2 = sample_route(
            source=airport2, destination=airport1, distance=800
        )

        res_list = self.client.get(ROUTE_URL)
        routes = Route.objects.all()
        serializer_list = RouteListSerializer(routes, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

        res_detail = self.client.get(detail_route_url(route1.id))
        serializer_detail = RouteRetrieveSerializer(route1)

        self.assertEquals(res_detail.status_code, status.HTTP_200_OK)
        self.assertEquals(res_detail.data, serializer_detail.data)

    def test_flight_list_and_detail(self):
        country1 = sample_country(name="Country1", code="C1")
        country2 = sample_country(name="Country2", code="C2")
        city1 = sample_city(country1, name="City1")
        city2 = sample_city(country2, name="City2")
        airport1 = sample_airport(city1, name="Airport1")
        airport2 = sample_airport(city2, name="Airport2")

        route1 = sample_route(
            source=airport1, destination=airport2, distance=500
        )
        route2 = sample_route(
            source=airport2, destination=airport1, distance=800
        )

        flight1 = sample_flight(route=route1, airplane_name="Test Airplane 1",
                                airplane_type_name="Test Airplane Type 1")
        flight2 = sample_flight(route=route2, airplane_name="Test Airplane 2",
                                airplane_type_name="Test Airplane Type 2")

        res_list = self.client.get(FLIGHT_URL)
        flights = Flight.objects.all()
        serializer_list = FlightListSerializer(flights, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

        res_detail = self.client.get(detail_flight_url(flight1.id))
        serializer_detail = FlightRetrieveSerializer(flight1)

        self.assertEquals(res_detail.status_code, status.HTTP_200_OK)
        self.assertEquals(res_detail.data, serializer_detail.data)

    def test_list_orders(self):
        order1 = sample_order(self.user)
        order2 = sample_order(self.user)

        res_list = self.client.get(ORDER_URL)
        orders = Order.objects.filter(user=self.user)
        serializer_list = OrderListSerializer(orders, many=True)

        self.assertEquals(res_list.status_code, status.HTTP_200_OK)
        self.assertEquals(res_list.data["results"], serializer_list.data)

    def test_create_order(self):
        flight = sample_flight()

        payload = {
            "tickets": [
                {"flight": flight.id, "row": 1, "seat": 1},
                {"flight": flight.id, "row": 2, "seat": 2},
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.user, self.user)

        tickets = Ticket.objects.filter(order=order)
        self.assertEqual(tickets.count(), 2)

        ticket_rows_seats = {(t.row, t.seat) for t in tickets}
        self.assertIn((1, 1), ticket_rows_seats)
        self.assertIn((2, 2), ticket_rows_seats)

    def test_retrieve_order_detail(self):
        order = sample_order(self.user)
        res = self.client.get(detail_order_url(order.id))
        serializer = OrderListSerializer(order)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)
