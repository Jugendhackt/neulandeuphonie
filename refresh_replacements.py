import requests
import json
req = requests.get("http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/replacements_by_word")
data = req.json()
rep = {}
for i in data['rows']:
    rep[i['key']] = []
    for value in i['value']:
        rep[i['key']].append(value)
with open("tag_replace/de.json", "w") as dictfile:
    json.dump(rep, dictfile, indent=4)
#import pdb;pdb.set_trace()
