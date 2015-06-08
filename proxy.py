#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8")
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
from requests_futures.sessions import FuturesSession
import replace_images
import sys
from bs4 import BeautifulSoup,Tag
session = FuturesSession(max_workers=10)
i=0
expression=[]

datei=open("dict.json")
stylesheet=open("style.css").read()
liste=json.load(datei)
expression = liste.items()
"""for key,value in liste.items():
    expression.append((re.compile(key, re.IGNORECASE |re.UNICODE), value))
    i=i+1
"""
regex_flags = re.IGNORECASE
class CensorMaster(controller.Master):
    def replaceText(self, key, value, text):
        change_dict = None
        subn_res = re.subn(key,value,text,flags=regex_flags)
        text = subn_res[0]
        #print(subn_res)
        #replaces = flow.response.replace(key,value_rand, flags=re.IGNORECASE)
        if subn_res[1] > 0:
            words = re.findall(key,text,flags=regex_flags)
            changes = {}
            for word in words:
                if word in changes:
                    changes[word] += 1
                else:
                    changes[word] = 1
            for change in changes:
                change_dict = {"word":"", "replaced_by":"", "count":"1"}
                change_dict['word'] = str(change)
                change_dict['replaced_by'] = str(value)
                change_dict['count'] = str(changes[change])
        return (text, change_dict)
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_response(self, flow):
        flow = replace_images.replaceImage(flow)
        try:
            stat = {"type":"statistic", "changes":[]}
            stat['url'] = flow.request.url
            attrs = dict((x.lower(),y) for x, y in flow.response.headers)
            if 'content-type' in attrs:
                if ('text/html' in attrs ['content-type']):

                    if 'content-encoding' in flow.response.headers.keys():
                        flow.response.content = flow.response.get_decoded_content()
                        del flow.response.headers['content-encoding']

                    page = BeautifulSoup(flow.response.get_decoded_content())
                    for key,value in expression:
                        value_rand = "(neulandeuphonie)"+random.choice(value)+"(/neulandeuphonie)"
                        for tag in page.findAll(text=re.compile(key, flags=regex_flags)):
                            
                            replace_data = self.replaceText(key,value_rand,unicode(tag.string))
                            """new_tag = page.new_tag("div")
                            new_tag["class"] = "neulandeuphonie"
                            new_tag.string = replace_data[0]
                            tag.string.replace_with(new_tag)"""
                            tag.string.replace_with(replace_data[0])
                            stat['changes'].append(replace_data[1])
                    if page.head != None:
                        new_tag = page.new_tag("style", type="text/css")
                        new_tag.string = stylesheet
                        page.head.append(new_tag)
                    flow.response.content = str(page)
                    flow.response.replace("\\(neulandeuphonie\\)","<span class=\"neulandeuphonie\">")
                    flow.response.replace("\\(/neulandeuphonie\\)","</span>")
                    #req = session.post("http://couchdb.pajowu.de/neulandeuphonie",data=json.dumps(stat),headers={'Content-type': 'application/json'})
        except Exception,e:
            print(e)
            #print (flow.response.get_decoded_content())
        flow.reply()
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
