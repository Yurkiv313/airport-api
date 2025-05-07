from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

from airport_app.models import Country, City, Airport, Route, AirplaneType, Airplane, Crew, Flight

fake = Faker()


class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **options):
        Country.objects.all().delete()
        City.objects.all().delete()
        Airport.objects.all().delete()
        Crew.objects.all().delete()
        Route.objects.all().delete()
        AirplaneType.objects.all().delete()
        Airplane.objects.all().delete()
        Flight.objects.all().delete()

        countries = [
            {"name": "Ukraine", "code": "UKR", "cities": ["Kyiv", "Lviv"]},
            {"name": "Germany", "code": "DEU", "cities": ["Berlin", "Munich"]},
            {"name": "USA", "code": "USA", "cities": ["New York", "Los Angeles"]},
            {"name": "France", "code": "FRA", "cities": ["Paris", "Nice"]},
        ]

        airports = []
        for country_data in countries:
            country = Country.objects.create(name=country_data["name"], code=country_data["code"])
            for city_name in country_data["cities"]:
                city = City.objects.create(name=city_name, country=country)
                airport = Airport.objects.create(name=fake.company(), city=city)
                airports.append(airport)

        airplane_types = []
        for name in ["Boeing 737", "Airbus A320", "Embraer E195", "Boeing 777", "Airbus A350"]:
            airplane_type = AirplaneType.objects.create(name=name)
            airplane_types.append(airplane_type)

        airplanes = []
        for airplane_type in airplane_types:
            for _ in range(2):
                airplane = Airplane.objects.create(
                    name=fake.word().title(),
                    rows=random.randint(20, 40),
                    seats_in_row=random.randint(4, 10),
                    airplane_type=airplane_type
                )
                airplanes.append(airplane)

        for _ in range(30):
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=random.choice(Crew.Position.choices)[0]
            )

        routes = []
        for _ in range(10):
            source, destination = random.sample(airports, 2)
            distance = random.randint(500, 10000)
            route = Route.objects.create(source=source, destination=destination, distance=distance)
            routes.append(route)

        for route in routes:
            airplane = random.choice(airplanes)
            while True:
                departure_time = timezone.now() + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
                arrival_time = departure_time + timedelta(hours=random.randint(2, 15))
                conflicting_flight = Flight.objects.filter(
                    airplane=airplane,
                    departure_time__date=departure_time.date(),
                    departure_time__lte=arrival_time,
                    arrival_time__gte=departure_time
                ).exists()
                if not conflicting_flight:
                    Flight.objects.create(
                        route=route,
                        airplane=airplane,
                        departure_time=departure_time,
                        arrival_time=arrival_time,
                        is_active=True
                    )
                    break

        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
