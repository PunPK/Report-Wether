import asyncio
import random
from Data import get_mock_weather
import aiofiles
import csv
from io import StringIO
import aiohttp

API_KEY = "your_openweathermap_api_key"  # API Key OpenWeatherMap ของผมไม่ได้ใส่นะครับ
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

MODE = "mock"


async def read_weather_data(file_path):
    data = []
    # ปรับใช้การดึงข้อมูลแบบ Asynchronous ครับ
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        content = await file.read()
        reader = csv.DictReader(StringIO(content))
        for row in reader:
            data.append(row)
    return data


async def fetch_weather_api(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"เกิดข้อผิดพลาดในการดึงข้อมูลสำหรับเมือง {city}")
                return None

    # สุ่มเวลาให้ดูเหมือนกำลังดึงข้อมูลแบบ Asynchronous ครับ
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return get_mock_weather(city)


async def fetch_weather_mock(city):
    # สุ่มเวลาให้ดูเหมือนกำลังดึงข้อมูลแบบ Asynchronous ครับ
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return get_mock_weather(city)


async def fetch_weather(city):

    if MODE == "csv":
        file_path = "Data/weather_data.csv"
        weather_data = await read_weather_data(file_path)
        for row in weather_data:
            if row["city"] == city:
                return {
                    "temp": int(row["temp"]),
                    "description": row["description"],
                    "humidity": int(row["humidity"]),
                }
        return None

    elif MODE == "mock":
        return await fetch_weather_mock(city)

    elif MODE == "api":
        return await fetch_weather_api(city)

    else:
        raise ValueError("โหมดไม่ถูกต้อง: ใช้ 'mock', 'csv', 'api' เท่านั้น")


async def display_weather(city):
    weather_data = await fetch_weather(city)
    if weather_data:
        print(f"\nข้อมูลสภาพอากาศสำหรับเมือง {city}:")
        print(f"อุณหภูมิ: {weather_data['temp']}°C")
        print(f"สภาพอากาศ: {weather_data['description']}")
        print(f"ความชื้น: {weather_data['humidity']}%")
    else:
        print(f"ไม่พบข้อมูลสำหรับเมือง {city}")


async def main():
    global MODE
    print(
        "Select Mode By \n  1. csv [File .CSV] \n  2. mock [Mock Data] \n  3. api [Fetch API]"
    )
    MODE = input("Choose Mode For Report: ")
    cities = [
        "Bangkok",
        "London",
        "New York",
        "Tokyo",
        "Paris",
        "Berlin",
        "Moscow",
        "Sydney",
        "Rio de Janeiro",
        "Dubai",
        "Mumbai",
        "Seoul",
        "Beijing",
        "Cairo",
        "Rome",
        "Bangladesh",
        "Madrid",
        "Jakarta",
        "Buenos Aires",
        "Cape Town",
    ]

    tasks = [display_weather(city) for city in cities]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
