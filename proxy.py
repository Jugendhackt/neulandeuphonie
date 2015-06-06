#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys);sys.setdefaultencoding("utf-8")
"""
This example builds on mitmproxy's base proxying infrastructure to
implement functionality similar to the "sticky cookies" option.
Heads Up: In the majority of cases, you want to use inline scripts.
"""
import os
import random
import json
import re
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import requests
i=0
expression=[]

datei=open("dict.json")
stylesheet=open("style.css").read()
liste=json.load(datei)
for key,value in liste.items():
    expression.append((re.compile((key), re.IGNORECASE), value))
    i=i+1


class CensorMaster(controller.Master):
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_response(self, flow):
        #import pdb;pdb.set_trace()
        print(flow.request.headers)
        try:
            stat = {"type":"statistic", "changes":[]}
            stat['url'] = flow.request.url
            attrs = dict((x.lower(),y) for x, y in flow.response.headers)
            if 'content-type' in attrs:
                if (attrs ['content-type'] == 'text/html'):
                    #flow.response.content += ("<style>" + stylesheet + "</style>")
                    tmp = flow.response.content.split("</head>") 
                    tmp[0]+="<style>" + stylesheet + "</style>" + "</head>"
                    flow.response.content = "".join(tmp)
        
                for key,value in expression:
                    change = {"word":"", "replaced_by":"", "count":"1"}
                    value_rand = random.choice(value)
                    subn_res = re.subn(key,value_rand,flow.response.content)
                    flow.response.content = subn_res[0]
                    #import pdb; pdb.set_trace()
                    flow.reply()
                    change['word'] = str(key.pattern)
                    change['replaced_by'] = (str(value_rand))
                    change['count'] = str(subn_res[1])
                    stat['changes'].append(change)
                req = requests.post("http://couchdb.pajowu.de/neulandeuphonie",data=json.dumps(stat),headers={'Content-type': 'application/json'})
        
        except UnicodeDecodeError, e:
            print (flow.response.content)
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
