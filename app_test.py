import requests
import json

# data for testing purposes
testing_data = {
  "actions": [
    {
      "type": "HTTPRequestAction",
      "name": "location",
      "options": {
        "url": "http://free.ipwhois.io/json/"
      }
    },
    {
      "type": "HTTPRequestAction",
      "name": "sunset",
      "options": {
        "url": "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}}"
      }
    },
    {
      "type": "PrintAction",
      "name": "print",
      "options": {
        "message": "Sunset in {{location.peter}}, {{location.country}} is at {{sunset.results.sunset}}."
      }
    }
  ]
}

# Convert test data to json format 
testing_json = json.dumps(testing_data)

# Function to confirm 200 status code
def test_status_code_equals_200():
    response = requests.get(testing_data['actions'][0]['options']['url'])
    assert response.status_code == 200

# Function to confirm action name
def test_name_equals_location():
    response = testing_data['actions'][0]
    assert response["name"] == "location"

# Function to confirm nasted data
def test_url_equals_address():
    response = testing_data['actions'][0]
    assert response['options']['url'] == "http://free.ipwhois.io/json/"