from faker import Faker
import random
import time

fake = Faker()


def fetch_data() -> list:
    """We will fetch a random number of geos"""
    data = []
    for i in range(random.randint(2, 8)):
        data.append(fake.location_on_land())

    time.sleep(1)  # Simulate taking time to hit an external API

    return data
