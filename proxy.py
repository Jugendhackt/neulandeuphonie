#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from mitmproxy import controller, proxy
from mitmproxy.proxy.server import ProxyServer
import proxy_functions
import threading
import configparser as ConfigParser
import glob
import os


class CensorMaster():
    def __init__(self, server):
        self.config = ConfigParser.ConfigParser()
        self.config.read(['default.ini', 'local.ini'])
        self.regex_flags = re.IGNORECASE
        self.tag_expressions = {"fallback": self.config.get("general", "fallback_language")}
        self.content_expressions = {"fallback": self.config.get("general", "fallback_language")}
        for filename in glob.glob("tag_replace/*.json"):
            with open(filename) as regex_file:
                lang = os.path.splitext(os.path.basename(filename))[0]
                self.tag_expressions[lang] = []
                regex_list = json.load(regex_file)
                for expression, replacement_text in regex_list.items():
                    compiled_expression = re.compile(expression, self.regex_flags)
                    self.tag_expressions[lang].append((compiled_expression, replacement_text))
        for filename in glob.glob("content_replace/*.json"):
            with open(filename) as regex_file:
                lang = os.path.splitext(os.path.basename(filename))[0]
                self.content_expressions[lang] = []
                regex_list = json.load(regex_file)
                for expression, replacement_text in regex_list.items():
                    compiled_expression = re.compile(expression, self.regex_flags)
                    self.content_expressions[lang].append((compiled_expression, replacement_text))
    print("started, listining on port 8080")

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_response(self, flow):
        def request_thread(flow):
            flow = proxy_functions.replaceImage(flow)
            flow = proxy_functions.censorText(flow, self.tag_expressions, self.content_expressions, self.config.get("general", "stylesheet_file"), self.config.getboolean("general", "send_stats"), self.config.getboolean("general","replace"))
            flow.reply()
        t = threading.Thread(target=request_thread, args=(flow,))
        t.daemonize = True
        t.start()
config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = CensorMaster(server)
m.run()
