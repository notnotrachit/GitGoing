import os
import logging
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import time

# load env variables & setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO, filename="weather.log", format="%(asctime)s - %(levelname)s - %(message)s")

def get_weather(city: str, api_key: str) -> dict:
    """
    Get weather data about the given city from the OpenWeatherMap API

    Args:
        city: the city to get weather about
        api_key: a *valid* api key for the OpenWeatherMap API

    Returns:
        a dictionary containing weather data about the given city, or
        an empty dictionary if an error occurred
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        # make request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.HTTPError:
        # http error e.g. 400
        logging.exception("Failed to get weather data from OpenWeatherMap.")
        st.error(f"Oops, we were unable to find weather data found for '{city}'! Please try again later.")
        return {}
    except (requests.Timeout, requests.ConnectionError):
        # failed to connect or took too long
        logging.exception("Request to OpenWeatherMap timed out.")
        st.error(f"Oops, the weather service seems to be down! Please try again later.")
        return {}
    except Exception as e:
        # catch all other potential errors
        logging.exception(f"An unexpected error occurred: {e}")
        st.error(f"Oops, something went wrong on our end! Please try again later.")
        return {}

    return response.json()

def main() -> None:
    """
    Main function that grabs weather data and runs the
    Weather Dashboard Streamlit app.
    """
    st.title("Weather Dashboard")
    
    # basic input for city
    city = st.text_input("Enter City Name", "London")
    
    # Placeholder for API key - This should be moved to environment variables
    api_key = os.getenv('API_KEY')
    if st.button("Get Weather"):
        if not api_key:
            st.error("Please enter an API key")
            return

        # get weather data
        weather_data = get_weather(city, api_key)
        if not weather_data:
            return
        
        try:
            # display basic weather information
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]

            st.write(f"Temperature: {temp}°C")
            st.write(f"Humidity: {humidity}%")
            st.write(f"Conditions: {description}")
            logging.info(f"Weather data for {city} retrieved successfully.")
        except KeyError:
            # handle missing/poorly formatted data
            st.error("Oops, some weather data is missing. Please try again later.")
            logging.exception("Failed to parse weather data.")

if __name__ == "__main__":
    main()
