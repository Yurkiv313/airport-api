from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

from django.apps import apps
from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
)

fake = Faker()

MODELS = [
    "Country",
    "City",
    "Crew",
    "Route",
    "AirplaneType",
    "Airplane",
    "Flight",
    "Ticket",
    "Order",
    "Airport",
]


class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **options):
        for model_name in MODELS:
            model = apps.get_model("airport_app", model_name)
            model.objects.all().delete()
            self.stdout.write(f"Deleted all {model_name} objects.")

        countries = [
            {"name": "Ukraine", "code": "UKR", "cities": ["Kyiv", "Lviv"]},
            {
                "name": "Germany",
                "code": "DEU",
                "cities": ["Berlin", "Munich"],
            },
            {
                "name": "USA",
                "code": "USA",
                "cities": ["New York", "Los Angeles"],
            },
            {"name": "France", "code": "FRA", "cities": ["Paris", "Nice"]},
        ]

        airports = []
        for country_data in countries:
            country = Country.objects.create(
                name=country_data["name"], code=country_data["code"]
            )
            for city_name in country_data["cities"]:
                city = City.objects.create(name=city_name, country=country)
                airport = Airport.objects.create(
                    name=f"{city_name} International", city=city
                )
                airports.append(airport)

        airplane_types = []
        for name in [
            "Boeing 737",
            "Airbus A320",
            "Embraer E195",
            "Boeing 777",
            "Airbus A350",
        ]:
            airplane_type = AirplaneType.objects.create(name=name)
            airplane_types.append(airplane_type)

        airplanes = []
        for airplane_type in airplane_types:
            for _ in range(2):
                airplane = Airplane.objects.create(
                    name=fake.word().title(),
                    rows=random.randint(20, 40),
                    seats_in_row=random.randint(4, 10),
                    airplane_type=airplane_type,
                )
                airplanes.append(airplane)

        main_pilots = [
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=Crew.Position.MAIN_PILOT,
            )
            for _ in range(3)
        ]
        second_pilots = [
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=Crew.Position.SECOND_PILOT,
            )
            for _ in range(3)
        ]
        medics = [
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=Crew.Position.MEDIC,
            )
            for _ in range(3)
        ]
        stewardesses = [
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=Crew.Position.STEWARDESS,
            )
            for _ in range(3)
        ]
        crew_members = [
            Crew.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=Crew.Position.CREW_MEMBER,
            )
            for _ in range(3)
        ]

        routes = []
        for _ in range(9):
            source, destination = random.sample(airports, 2)
            distance = random.randint(500, 10000)
            route = Route.objects.create(
                source=source, destination=destination, distance=distance
            )
            routes.append(route)

        for i in range(9):
            route = routes[i]
            airplane = airplanes[i % len(airplanes)]
            departure_time = timezone.now() + timedelta(
                days=i * 2, hours=random.randint(0, 23)
            )
            arrival_time = departure_time + timedelta(
                hours=random.randint(2, 10)
            )

            flight = Flight.objects.create(
                route=route,
                airplane=airplane,
                departure_time=departure_time,
                arrival_time=arrival_time,
                is_active=True,
            )
            flight.crew.add(
                main_pilots[i % len(main_pilots)],
                second_pilots[i % len(second_pilots)],
                medics[i % len(medics)],
                stewardesses[i % len(stewardesses)],
                crew_members[i % len(crew_members)],
            )
            flight.save()

        self.stdout.write(
            self.style.SUCCESS("Database populated successfully.")
        )
