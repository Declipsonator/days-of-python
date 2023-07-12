import requests


def get_weather(location):
    api_key = "c0e7f96d4f39fff2b865691d04447575"  # Replace with your Weatherstack API key
    base_url = f"http://api.weatherstack.com/current"
    params = {
        "access_key": api_key,
        "query": location
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def display_weather(data):
    if "current" in data:
        name = data["location"]["name"]
        temperature = data["current"]["temperature"]
        description = data["current"]["weather_descriptions"][0]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_speed"]

        print(f"Weather in {name}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {description}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} km/h")
    else:
        print("Failed to fetch weather data.")


def main():
    location = input("Enter a location: ")
    weather_data = get_weather(location)
    display_weather(weather_data)


if __name__ == "__main__":
    main()
