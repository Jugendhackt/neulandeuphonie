#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8") # hack to set default encoding
import json
import re
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import proxy_functions
import threading
import ConfigParser
class CensorMaster(controller.Master):
    def __init__(self,server):
        controller.Master.__init__(self, server)
        self.config = ConfigParser.ConfigParser()
        self.config.read(['default.ini','local.ini'])
        self.regex_flags = re.IGNORECASE
        with open("tag_expressions.json") as regex_file:
            regex_list=json.load(regex_file)
            self.tag_expressions = []
            for expression,replacement_text in regex_list.items():
                compiled_expression = re.compile(expression,self.regex_flags)
                self.tag_expressions.append((compiled_expression,replacement_text))
        with open("content_expressions.json") as regex_file:
            regex_list=json.load(regex_file)
            self.content_expressions = []
            for expression,replacement_text in regex_list.items():
                compiled_expression = re.compile(expression,self.regex_flags)
                self.content_expressions.append((compiled_expression,replacement_text))
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()
    def handle_response(self, flow):
        def request_thread(flow):
            flow = proxy_functions.replaceImage(flow)
            flow = proxy_functions.censorText(flow,self.tag_expressions,self.content_expressions,self.config.get("general","stylesheet_file"),self.config.getboolean("general","send_stats"))
            flow.reply()
        t = threading.Thread(target=request_thread, args=(flow,))
        t.daemonize = True
        t.start()
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
