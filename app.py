import sys
import json
import requests
import re


# Function for HTTPRequestAction call
def requestAction(action, data):
    url = action['options']['url']
    # if url contains interpolated values, use function
    if "{{" and "}}" in url:
        url = interpolation(url, storedData)
    r = requests.get(url)
    # if 2xx HTTP response gather request data
    if r.status_code == 200 or 204:
        storedData2 = r.text
        parse_json = json.loads(storedData2)
        return parse_json
    # implement Network failure and termination for non-2xx HTTP response
    else:
        print('Network Failure. Terminating Program')
        sys.exit()


# Function to interpolate values to string/url
def interpolation(string, inputData):
    # identify and store values between dounble curly braces
    text_in_brackets = re.findall('[^{\{]+(?=}\})', string)
    keys = []
    values = []
    # loop to split values
    for i in text_in_brackets:
        keys.append(i.split("."))
    # double loop to identify and store keys values from HTTPRequest data
    for j in range(0, len(keys)):
        temp = storedData
        for k in range(0, len(keys[j])):
            # try except to store found data and store blank if key not valued
            try:
                temp = temp[keys[j][k]]
            except:
                temp = ''
        values.append(temp)
    # iterate through string and replace curly braces keys with stored values
    for l in range(0, len(text_in_brackets)):
        string = string.replace(
            "{{"+str(text_in_brackets[l])+"}}", str(values[l]))
    return string


# locate json file from command line argument
filename = "datafiles/" + sys.argv[1]
try:
    with open(filename) as json_file:
        # gather data from data file and convert to json format
        actionsObject = json.load(json_file)
        # object to store all HTTPRequestAction data
        storedData = {}
        # iterate through actions to store & trigger function depending on type
        for action in actionsObject['actions']:
            if action['type'] == "HTTPRequestAction":
                # Request data and store with actions name as value
                storedData[action['name']] = requestAction(action, storedData)
            if action['type'] == "PrintAction":
                # Gather string, interpolate and print to console
                printString = action['options']['message']
                message = interpolation(printString, storedData)
                print(message)
# implement Network failure and termination if file not located
except FileNotFoundError:
    print('Invalid file name.')
    sys.exit()
