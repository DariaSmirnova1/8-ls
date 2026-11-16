import requests


# Словарь погодных условий
WEATHER_CODES = {
    0: "☀️ Ясно",
    1: "🌤️ Преимущественно ясно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫️ Туман",
    48: "🌫️ Иней",
    51: "🌦️ Легкая морось",
    53: "🌦️ Морось",
    55: "🌧️ Сильная морось",
    61: "🌧️ Небольшой дождь",
    63: "🌧️ Дождь",
    65: "🌧️ Сильный дождь",
    71: "🌨️ Небольшой снег",
    73: "🌨️ Снег",
    75: "🌨️ Сильный снег",
    80: "🌦️ Ливень",
    95: "⛈️ Гроза",
    96: "⛈️ Гроза с градом"
}


# Функция получения координат города
def get_city_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1,
        "language": "ru"
    }

    try:
        print("\nПолучаем координаты города...")

        response = requests.get(
            url,
            params=params,
            timeout=(10, 30)
        )

        response.raise_for_status()
        data = response.json()

        results = data.get("results")

        if not results:
            print(
                f"Город '{city_name}' не найден. "
                "Проверьте название."
            )
            return None

        lat = results[0]["latitude"]
        lon = results[0]["longitude"]

        print("Координаты успешно получены!")

        return lat, lon

    except requests.exceptions.Timeout:
        print("Ошибка: превышено время ожидания запроса.")

    except requests.exceptions.HTTPError:
        print("Ошибка HTTP при получении координат.")

    except requests.exceptions.ConnectionError:
        print("Ошибка сети. Проверьте интернет.")

    except ValueError:
        print("Ошибка: получен невалидный JSON.")

    except (KeyError, IndexError, TypeError):
        print("Ошибка: некорректные данные о городе.")

    return None


# Функция получения погоды
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "timezone": "auto"
    }

    try:
        print("\nПолучаем информацию о погоде...")

        response = requests.get(
            url,
            params=params,
            timeout=(10, 30)
        )

        response.raise_for_status()
        data = response.json()

        weather = data.get("current")

        if not weather:
            print("Ошибка: данные о погоде отсутствуют.")
            return None

        print("Погода успешно получена!")

        return weather

    except requests.exceptions.Timeout:
        print("Ошибка: превышено время ожидания запроса.")

    except requests.exceptions.HTTPError:
        print("Ошибка HTTP при получении погоды.")

    except requests.exceptions.ConnectionError:
        print("Ошибка сети. Проверьте интернет.")

    except ValueError:
        print("Ошибка: получен невалидный JSON.")

    except (KeyError, TypeError):
        print("Ошибка: некорректные данные о погоде.")

    return None


# Функция расшифровки погодного кода
def decode_weather_code(code):
    return WEATHER_CODES.get(
        code,
        f"Неизвестные условия (код: {code})"
    )


# Функция форматирования результата
def format_weather_output(city, weather_data):
    temperature = weather_data["temperature_2m"]
    humidity = weather_data["relative_humidity_2m"]
    wind = weather_data["wind_speed_10m"]
    code = weather_data["weather_code"]

    condition = decode_weather_code(code)

    result = (
        "\n" + "=" * 42 + "\n"
        f"       ПОГОДА В ГОРОДЕ: {city.upper()}\n"
        + "=" * 42 + "\n"
        f"Температура:   {temperature:+.1f} °C\n"
        f"Влажность:     {humidity} %\n"
        f"Ветер:         {wind} км/ч\n"
        f"Состояние:     {condition}\n"
        + "=" * 42
    )

    return result


# Главная функция программы
def main():
    print("=" * 42)
    print("          ПРОГНОЗ ПОГОДЫ")
    print("=" * 42)

    city = input(
        "Введите название города на английском: "
    ).strip()

    # Проверка пустого ввода
    if not city:
        print("Ошибка: название города не может быть пустым.")
        return

    # Получаем координаты
    coordinates = get_city_coordinates(city)

    if coordinates is None:
        return

    lat, lon = coordinates

    # Получаем погоду
    weather_data = get_weather(lat, lon)

    if weather_data is None:
        return

    # Выводим результат
    print(format_weather_output(city, weather_data))


# Запуск программы
if __name__ == "__main__":
    main()
