import random

mock_weather_data = {
    "Bangkok": {"temp": 32, "description": "sunny", "humidity": 60},
    "London": {"temp": 15, "description": "cloudy", "humidity": 75},
    "New York": {"temp": 22, "description": "partly cloudy", "humidity": 65},
    "Tokyo": {"temp": 27, "description": "clear", "humidity": 70},
    "Paris": {"temp": 18, "description": "rainy", "humidity": 80},
    "Berlin": {"temp": 25, "description": "sunny", "humidity": 68},
    "Moscow": {"temp": 10, "description": "snowy", "humidity": 85},
    "Sydney": {"temp": 28, "description": "hot", "humidity": 55},
    "Rio de Janeiro": {"temp": 30, "description": "sunny", "humidity": 75},
    "Dubai": {"temp": 38, "description": "hot", "humidity": 40},
    "Mumbai": {"temp": 34, "description": "humid", "humidity": 85},
    "Seoul": {"temp": 24, "description": "clear", "humidity": 60},
    "Beijing": {"temp": 20, "description": "cloudy", "humidity": 65},
    "Cairo": {"temp": 35, "description": "dry", "humidity": 20},
    "Rome": {"temp": 26, "description": "sunny", "humidity": 55},
}


def get_mock_weather(city):
    if city in mock_weather_data:
        return mock_weather_data[city]
    else:
        return {
            "temp": random.randint(10, 40),
            "description": random.choice(
                [
                    "sunny",
                    "cloudy",
                    "rainy",
                    "clear",
                    "partly cloudy",
                    "hot",
                    "humid",
                    "dry",
                ]
            ),
            "humidity": random.randint(20, 90),
        }
