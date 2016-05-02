# -*- coding: utf-8 -*-
import urllib
import urllib2

domian = "http://demo.bibifa.com"

deviceid = "7c37c497a5bb11e3a0cb60c54707f514"
def setplayhistory():
    cmd = "setplayhistory"
    mediaid = 12345
    ci = 1
    url = "http://test.com"
    playtime = 10000
    print domian+"/setplayhistory?deviceid=7c37c497a5bb11e3a0cb60c54707f514&mediaid=12345&ci=1&url="+urllib.quote(url)+"&playtime=10000"
    print urllib2.urlopen(domian+"/setplayhistory?deviceid=7c37c497a5bb11e3a0cb60c54707f514&mediaid=12345&ci=1&url="+urllib.quote(url)+"&playtime=10000").read()

def getplayhistory():
    print urllib2.urlopen(domian+"/getplayhistory?deviceid=7c37c497a5bb11e3a0cb60c54707f514").read()

def deleteplayhistory():
    print urllib2.urlopen(domian+"/deleteplayhistory?deviceid=7c37c497a5bb11e3a0cb60c54707f514").read()


if __name__ == "__main__":
    setplayhistory()
    getplayhistory()
    #deleteplayhistory()
    #getplayhistory()

