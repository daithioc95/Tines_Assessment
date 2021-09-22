import sys
import json
import requests
import re

# An Action is described in the Story file by an object with the keys type , name and options
# A Story is executed by running its Actions in the order that they appear in the Story file. When run, 
# each Action produces an output Event, which is then passed to the next Action as its input Event
# when it is run, and so on.

filename = "datafiles/" + sys.argv[1]


def ActionRequest(action):
    r =requests.get(action['options']['url'])
    storedData2 = r.text
    parse_json = json.loads(storedData2)
    # print(parse_json['ip'])
    return parse_json


# def urlInterpolation(url, inputdata):
#      # s_without_parens = re.sub('\(.+?\)','',url)
#     text_in_brackets = re.findall('[^{\{]+(?=}\})',url)
#     keys=[]
#     values=[]
#     for i in text_in_brackets:
#         keys.append(i.split(".")[0])
#         values.append(i.split(".")[1])
#     for value in inputdata:
#         print("value")

with open(filename) as json_file:
    actionsObject = json.load(json_file)
    storedData = {}
    for action in actionsObject['actions']:
        if action['type'] == "HTTPRequestAction":
            # actionData = {action['name']:ActionRequest(action)}
            # storedData.append(actionData)
            storedData[action['name']] = ActionRequest(action)
            parse_json2 = json.dumps(storedData)
    print(storedData['location']['ip'])

        # for x in storedData:
        #     if action['name'] == list(x)[0]:
        #         print(x)
# print(storedData)

    # print(storedData[0]['location']['ip'])
            # r =requests.get(action['options']['url'])
            # print(r)
            # if "{{" and "}}" in url:
            #     urlInterpolation(url, storedData)
            #     # print(storedData)
            # else:
            #     print("no interpolation")
