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
        try:
            attrs = dict((x.lower(),y) for x, y in flow.response.headers)
            if 'content-type' in attrs:
                print "content type"
                if (attrs ['content-type'] == 'text/html'):
                    print "html/css"
                    #flow.response.content += ("<style>" + stylesheet + "</style>")
                    tmp = flow.response.content.split("</head>") 
                    tmp[0]+="<style>" + stylesheet + "</style>" + "</head>"
                    flow.response.content = "".join(tmp)
        
                for key,value in expression:
                    value_rand = random.choice(value)
                    flow.response.content = re.sub(key,value_rand,flow.response.content)
                    #import pdb; pdb.set_trace()
                    flow.reply()
        
        except UnicodeDecodeError, e:
            print (flow.response.content)
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
