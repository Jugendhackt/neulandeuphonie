#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8") # hack to set default encoding
import json
import re
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import proxy_functions
class CensorMaster(controller.Master):
    def __init__(self,server):
        controller.Master.__init__(self, server)
        with open("dict.json") as regexfile:
            regex_list=json.load(regexfile)
            self.expressions = regex_list.items()
        with open("style.css") as stylesheet_file:
            self.stylesheet = stylesheet_file.read()
        self.regex_flags = re.IGNORECASE
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_response(self, flow):
        flow = proxy_functions.replaceImage(flow)
        flow = proxy_functions.censorText(flow,self.expressions,self.stylesheet,self.regex_flags)
        flow.reply()
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
