import sys
import json
import requests
import re

# An Action is described in the Story file by an object with the keys type , name and options
# A Story is executed by running its Actions in the order that they appear in the Story file. When run, 
# each Action produces an output Event, which is then passed to the next Action as its input Event
# when it is run, and so on.

filename = "datafiles/" + sys.argv[1]


def requestAction(action, data):
    url = action['options']['url']
    if "{{" and "}}" in url:
        url = urlInterpolation(url, storedData)
    r =requests.get(url)
    storedData2 = r.text
    parse_json = json.loads(storedData2)
    return parse_json


def urlInterpolation(url, inputdata):
    text_in_brackets = re.findall('[^{\{]+(?=}\})',url)
    keys=[]
    values = []
    for i in text_in_brackets:
        url = url.replace("{"+str(i)+"}",'')
        keys.append(i.split("."))
    for j in range(0,len(keys)):
        temp = storedData
        for k in range(0,len(keys[j])):
            temp=temp[keys[j][k]]
        values.append(temp)
    url = url.format(*values)
    return url


with open(filename) as json_file:
    actionsObject = json.load(json_file)
    storedData = {}
    for action in actionsObject['actions']:
        if action['type'] == "HTTPRequestAction":
            storedData[action['name']] = requestAction(action, storedData)
        if action['type'] == "PrintAction":
            message = urlInterpolation(action['options']['message'], storedData)
            print(message)
# interpolate message action