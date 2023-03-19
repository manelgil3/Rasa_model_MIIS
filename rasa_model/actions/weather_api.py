import requests

def get_temperature_barcelona(api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Barcelona&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        return temperature
    else:
        print(f"Error: {response.status_code}")
        return None
