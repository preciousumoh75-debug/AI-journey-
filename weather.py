import requests 

city = input("input city: ")
url = f"http://wttr.in/{city}?format=%l:+%t+%C"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        print(response.text.strip())
    else:
        print("City not found or service error.")
except Exception as e:
    print(f"Error connecting: {e}")