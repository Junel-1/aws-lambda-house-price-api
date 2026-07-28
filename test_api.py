import requests

url = "http://127.0.0.1:8000/predict"

sample_house = {
    "sqft": 2200,
    "bedrooms": 3,
    "bathrooms": 2.5
}

response = requests.post(url, json=sample_house)
print("Response from API:")
print(response.json())