import os
import logging
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# load env variables & setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO, filename="weather.log", format="%(asctime)s - %(levelname)s - %(message)s")

def get_weather(city, api_key):
    """
    Get weather data from OpenWeatherMap API
    Note: This function needs a valid API key to work
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
        st.error(f"Oops, e were unable to find weather data found for '{city}'! Please try again later.")
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

def main():
    st.title("Weather Dashboard")
    
    # Basic input for city
    city = st.text_input("Enter City Name", "London")
    
    api_key = os.getenv("API_KEY")
    
    if st.button("Get Weather"):
        if not api_key:
            st.error("Please enter an API key")
            return
            
        weather_data = get_weather(city, api_key)
        if not weather_data:
            # check we got weather data
            return
        
        try:
            # Display basic weather information
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
