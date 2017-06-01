import proxy_functions
import configparser as ConfigParser
import glob, os, re, json
config = ConfigParser.ConfigParser()
config.read(['default.ini', 'local.ini'])
regex_flags = re.IGNORECASE
tag_expressions = {"fallback": config.get("general", "fallback_language")}
content_expressions = {"fallback": config.get("general", "fallback_language")}
for filename in glob.glob("tag_replace/*.json"):
    with open(filename) as regex_file:
        lang = os.path.splitext(os.path.basename(filename))[0]
        tag_expressions[lang] = []
        regex_list = json.load(regex_file)
        for expression, replacement_text in regex_list.items():
            compiled_expression = re.compile(expression, regex_flags)
            tag_expressions[lang].append((compiled_expression, replacement_text))
for filename in glob.glob("content_replace/*.json"):
    with open(filename) as regex_file:
        lang = os.path.splitext(os.path.basename(filename))[0]
        content_expressions[lang] = []
        regex_list = json.load(regex_file)
        for expression, replacement_text in regex_list.items():
            compiled_expression = re.compile(expression, regex_flags)
            content_expressions[lang].append((compiled_expression, replacement_text))

def response(flow):
    flow = proxy_functions.replaceImage(flow)
    flow = proxy_functions.censorText(flow, tag_expressions, content_expressions, config.get("general", "stylesheet_file"), config.getboolean("general", "send_stats"), config.getboolean("general","replace"))
    #flow.reply()
    return flow


def handle_response(*args, **kwargs):
    print(args, kwargs)
