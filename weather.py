import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8' )
import requests 
city = input("Enter city (or press Enter for Default): ")
if city == "":
    city = "Ikot ekpene"
url = f"https://wttr.in/{city}"
try:
    response = requests.get(url, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        weather_info = response.text.strip()
        print(weather_info)
        with open ("last_weather.txt", "w") as f:
            f.write(weather_info)
            f.write(weather_info)
    else:
        print(f"Error: API returned status {response.status_code}")
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error connecting: {e}")