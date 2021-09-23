import sys
import json
import requests
import re

# An Action is described in the Story file by an object with the keys type , name and options
# A Story is executed by running its Actions in the order that they appear in the Story file. When run, 
# each Action produces an output Event, which is then passed to the next Action as its input Event
# when it is run, and so on.

filename = "datafiles/" + sys.argv[1]


def ActionRequest(action, data):
    url = action['options']['url']
    if "{{" and "}}" in url:
        urlInterpolation(url, storedData)
    else:
        r =requests.get(url)
        storedData2 = r.text
        parse_json = json.loads(storedData2)
        return parse_json


def urlInterpolation(url, inputdata):
     # s_without_parens = re.sub('\(.+?\)','',url)
    text_in_brackets = re.findall('[^{\{]+(?=}\})',url)
    keys=[]
    values = []
    for i in text_in_brackets:
        keys.append(i.split("."))
    for j in range(0,len(keys)):
        temp = storedData
        for k in range(0,len(keys[j])):
            temp=temp[keys[j][k]]
        values.append(temp)
    print(values)


            # print(storedData['location']['latitude'])

    # try mapping??
    # print(*map(storedData.get, keys[1]))


    # for i in keys:
    #     if len(i)==2:
    #         print(storedData[i[0]][i[1]])
    #     elif len(i)==3:
    #         print(storedData[i[0]][i[1]][i[0]])

    # for i in range(0,len(keys)):
    #     for j in keys[i]:
    #         for x in storedData:
    #             if j==x:
    #                 for l in keys[i]:
    #                     for y in storedData[x]:
    #                         if l==y:
    #                             print(storedData[x][l])
    
    # for item in keys:
    #     for i in range(0,len(keys)-1):
    #         print(item[i])
    #         print(item[i+1])
    #         print(storedData[item[i]][item[i+1]])
    # print(keys)
    # print(storedData[keys[0][0]][keys[0][1]])

with open(filename) as json_file:
    actionsObject = json.load(json_file)
    storedData = {}
    for action in actionsObject['actions']:
        if action['type'] == "HTTPRequestAction":
            storedData[action['name']] = ActionRequest(action, storedData)

    # print(storedData[0]['location']['ip'])
            # r =requests.get(action['options']['url'])
            # print(r)
            # if "{{" and "}}" in url:
            #     urlInterpolation(url, storedData)
            #     # print(storedData)
            # else:
            #     print("no interpolation")
