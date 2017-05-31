import json
import urllib


def getUvaInfo(username):
    url = "http://uhunt.felix-halim.net/api/uname2uid/"+username
    result = json.load(urllib.urlopen(url))
    url  = "http://uhunt.felix-halim.net/api/ranklist/"+str(result)+"/0/0"
    info  = json.load(urllib.urlopen(url))
    class UvaInfo(object):
        pass
    x = UvaInfo()
    x.name = info[0]["name"]
    x.rank = info[0]["rank"]
    x.nos = info[0]["nos"]
    x.ac = info[0]["ac"]
    if info[0]["activity"][0]>0:
        x.last = "last solved less than 2 days ago"
    elif info[0]["activity"][1]>0:
        x.last = "last solved less than 7 days ago"
    elif info[0]["activity"][2]>0:
        x.last = "last solved less than 1 month ago"
    elif info[0]["activity"][3]>0:
        x.last = "last solved less than 3 month ago"
    elif info[0]["activity"][4]>0:
        x.last = "last solved less than 1 year ago"
    else :
        x.last = "last solved more than 1 year ago"
    url = "http://uhunt.felix-halim.net/api/p"
    result = json.load(urllib.urlopen(url))
    a = dict(str(result[0][0])=result[0][2])
    print "-----------------------------"
    return x
