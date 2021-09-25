import sys
import json
import requests
import re


filename = "datafiles/" + sys.argv[1]


def requestAction(action, data):
    url = action['options']['url']
    if "{{" and "}}" in url:
        url = interpolation(url, storedData)
    r =requests.get(url)
    if r.status_code == 200 or 204:
        storedData2 = r.text
        parse_json = json.loads(storedData2)
        return parse_json
    else:
        print('Network Failure. Terminating Program')
        sys.exit()

# if value doesn't exist in stored data, 
def interpolation(string, inputData):
    text_in_brackets = re.findall('[^{\{]+(?=}\})',string)
    keys=[]
    values = []
    for i in text_in_brackets:
        keys.append(i.split("."))
    for j in range(0,len(keys)):
        temp = storedData
        for k in range(0,len(keys[j])):
            try:
                temp=temp[keys[j][k]]
            except:
                temp=''
        values.append(temp)
    for l in range(0,len(text_in_brackets)):
        string = string.replace("{{"+str(text_in_brackets[l])+"}}",str(values[l]))
    return string

try:
    with open(filename) as json_file:
        actionsObject = json.load(json_file)
        storedData = {}
        for action in actionsObject['actions']:
            if action['type'] == "HTTPRequestAction":
                storedData[action['name']] = requestAction(action, storedData)
            if action['type'] == "PrintAction":
                printString = action['options']['message']
                message = interpolation(printString, storedData)
                print(message)
except FileNotFoundError:
    print('Invalid file name.')
    sys.exit()