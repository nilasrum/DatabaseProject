import json
import urllib


def getUvaInfo(username):
    url = "http://uhunt.felix-halim.net/api/uname2uid/"+username
    result = json.load(urllib.urlopen(url))
    id=result
    url  = "http://uhunt.felix-halim.net/api/ranklist/"+str(result)+"/0/0"
    info  = json.load(urllib.urlopen(url))
    class UvaInfo(object):
        pass
    x = UvaInfo()
    x.name = info[0]["name"]
    x.rank = info[0]["rank"]
    x.nos = info[0]["nos"]
    x.ac = info[0]["ac"]
    x.list = list()
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
    myMap = dict()
    for r in result:
        myMap[r[0]]=r[2]

    url = "http://uhunt.felix-halim.net/api/subs-user-last/"+str(id)+"/"+str(x.nos)
    result = json.load(urllib.urlopen(url))
    #print result
    for r in result["subs"]:
        if r[2]==90:
            x.list.append(" [ "+myMap[r[1]]+" ] ")
    return x



def getCfInfo(username):
    url = "http://codeforces.com/api/user.info?handles="+username
    result = json.load(urllib.urlopen(url))
    result = result["result"][0]
    class CfInfo(object):
        pass
    x = CfInfo()
    x.cur = str(result["rating"])+" ("+result["rank"]+")"
    x.max = str(result["maxRating"])+" ("+result["maxRank"]+")"
    x.name = result["firstName"]+" "+result["lastName"]
    x.list = list()
    url = "http://codeforces.com/api/user.rating?handle="+username
    result = json.load(urllib.urlopen(url))
    result = result["result"]
    for r in result:
        x.list.append(r["contestName"]+" ----- "+str(r["rank"])+" ----- "+str(r["newRating"]))

    return x
