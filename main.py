import os
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

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
    
    response = requests.get(base_url, params=params)
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
            
        try:
            weather_data = get_weather(city, api_key)
            
            if weather_data.get("cod") != 200:
                st.error(f"Error: {weather_data.get('message', 'Unknown error')}")
                return
                
            # Display basic weather information
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]
            
            st.write(f"Temperature: {temp}°C")
            st.write(f"Humidity: {humidity}%")
            st.write(f"Conditions: {description}")
            
        except requests.exceptions.RequestException:
            st.error("Failed to fetch weather data. Please try again.")
        except KeyError:
            st.error("Error parsing weather data")
            
if __name__ == "__main__":
    main()
