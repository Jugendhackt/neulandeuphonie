#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8") # hack to set default encoding
import json
import re
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import proxy_functions
import threading
class CensorMaster(controller.Master):
    def __init__(self,server):
        controller.Master.__init__(self, server)
        self.regex_flags = re.IGNORECASE
        with open("dict.json") as regexfile:
            regex_list=json.load(regexfile)
            self.expressions = []
            for expression,replacement_text in regex_list.items():
                compiled_expression = re.compile(expression,self.regex_flags)
                self.expressions.append((compiled_expression,replacement_text))
        with open("style.css") as stylesheet_file:
            self.stylesheet = stylesheet_file.read()
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()
    def handle_response(self, flow):
        def request_thread(flow):
            flow = proxy_functions.replaceImage(flow)
            flow = proxy_functions.censorText(flow,self.expressions,self.stylesheet)
            flow.reply()
        t = threading.Thread(target=request_thread, args=(flow,))
        t.daemonize = True
        t.start()
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
