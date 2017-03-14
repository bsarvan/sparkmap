import os
import sys
import urllib2
from PIL import Image

url = "https://maps.googleapis.com/maps/api/staticmap"
size = "zoom=13&size=600x300&maptype=roadmap"
api_key = "ZWM4ZTczMDgtMmVhZC00MWQwLTg5NGMtZmIyNWJmNTMwOTkwZDAwZTg2YjctNzQz"

def sendSparkPOST(url, data):
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents


def getStaticMap(location):
    url2 = url + '?center=' + location + size
    print url2

    request = urllib2.Request(url2,
                              headers = {"Accept":"image/png"})

    request.add_header("Authorization", "Bearer "+api_key);
    contents = urllib2.urlopen(request).read()
    return contents

@post('/index.json')
def index(request):
    bot_response = ""
    response = ""

    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    print result.get('text','')
    message = result.get('text','')

    if message == 'image':
        pic = getStaticMap('Belgaum')
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": pic})

    return "true"


if __name__ == "__main__":   
    run_itty(server='wsgiref', host='0.0.0.0', port=8080)
