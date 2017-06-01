import re
from PIL import Image
import io
import requests
import os
import random
import sys
from mitmproxy.http import HTTPResponse
import io
from bs4 import BeautifulSoup, NavigableString
import linecache


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def getsizes(image_data):
    p = Image.frombytes(image_data)
    return p.image.size


def resizeImg(sourceFile, width, height):
    img = Image.open(sourceFile)
    """if width > height:
        img.transform(resize="%d" % (width))
    else:
        img.transform(resize="x%d" % (height))"""
    img.thumbnail((width, height))
    wd = img.width - width
    hd = img.height - height
    img.crop((wd / 2, hd / 2, width, height))
    img.format = 'jpeg'
    return img


def replaceImage(flow):
    attrs = dict((x.lower(), y) for x, y in flow.response.headers.items())
    if "content-type" in attrs:
        if "image" in attrs['content-type'] and not "svg" in attrs['content-type']:
            if flow.response.status_code == 304:
                content = flow.response.content
            else:
                content = requests.get(flow.request.url).content
            if len(content) == 0:
                return flow
            try:
                img = Image.open(io.BytesIO(content))
                size = img.size
                if size[0] > 40 and size[1] > 40:
                    filename = random.choice(os.listdir("images"))
                    img = resizeImg("images/" + filename, size[0], size[1])
                    #content = img.make_blob()
                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr, format='JPEG')
                    content = imgByteArr.getvalue()
                    responseHeaders = {'Content-Length':str(len(content))}
                    responseHeaders['Content-Type'] = "image/jpg"
                    #import pdb;pdb.set_trace()
                    resp = HTTPResponse.make(status_code=200, headers=responseHeaders, content=content)
                    flow.response = resp

            except:
                PrintException()
    return flow


def adjustCasing(original, to_adjust):
    if original.group()[0].isupper():
        adjusted = "(neulandeuphonie)" + to_adjust.capitalize() + "(/neulandeuphonie)"
    else:
        adjusted = "(neulandeuphonie)" + to_adjust[0].lower() + to_adjust[1:] + "(/neulandeuphonie)"
    return adjusted


def censorText(flow, tag_expressions, content_expressions, stylesheet, send_stats, replace=False):
    attrs = dict((x.lower(), y) for x, y in flow.response.headers.items())
    if 'content-type' in attrs:
        if ('text/html' in attrs['content-type']):
            if send_stats:
                stat = {"type": "statistic", "changes": []}
                stat['url'] = flow.request.url
            flow.response.headers['content-type'] = "text/html"
            if 'content-encoding' in list(flow.response.headers.keys()):
                import pdb;pdb.set_trace()
                flow.response.content = flow.response.get_decoded_content()
                del flow.response.headers['content-encoding']
            page = BeautifulSoup(flow.response.content.decode())
            lang = detectLanguage(page)
            lang = lang if lang in tag_expressions or lang in content_expressions else tag_expressions['fallback']
            if lang in tag_expressions:
                for tag in page.findAll(text=True):
                    if type(tag) == NavigableString:
                        string = str(tag.string)
                        for key, value in tag_expressions[lang]:
                            value_rand = random.choice(value)
                            if not replace:
                                replace_data = replaceText(key, r'(neulandeuphonie)\g<0>(/neulandeuphonie)', string, send_stats)
                            else:
                                replace_data = replaceText(key, lambda x: adjustCasing(x, value_rand), string, send_stats)
                            string = replace_data[0]
                            if send_stats:
                                stats['changes'].append(replace_data[1])
                        tag.string.replace_with(string)
            page = injectCSS(page, stylesheet)
            flow.response.set_content(str(page).encode())
            if lang in content_expressions:
                for key, value in content_expressions[lang]:
                    flow.response.content = re.sub(key, random.choice(value), flow.response.content)

            flow.response.replace("\\(neulandeuphonie\\)","<span class=\"neulandeuphonie\">")
            flow.response.replace("\\(/neulandeuphonie\\)","</span>")
            if send_stats:
                req = session.post("http://couchdb.pajowu.de/neulandeuphonie", data=json.dumps(stat), headers={'Content-type': 'application/json'})
    return flow


def replaceText(key, value, text, send_stats=False):
    change_dict = None
    # print(subn_res)
    #replaces = flow.response.replace(key,value_rand, flags=re.IGNORECASE)
    if send_stats:
        subn_res = re.subn(key, value, text)
        text = subn_res[0]
        if subn_res[1] > 0:
            words = re.findall(key, text)
            changes = {}
            for word in words:
                if word in changes:
                    changes[word] += 1
                else:
                    changes[word] = 1
            for change in changes:
                change_dict = {"word": "", "replaced_by": "", "count": "1"}
                change_dict['word'] = str(change)
                change_dict['replaced_by'] = str(value)
                change_dict['count'] = str(changes[change])
    else:
        text = re.sub(key, value, text)
    return (text, change_dict)


def injectCSS(page, css_file):
    if type(page) != BeautifulSoup:
        page = BeautifulSoup(page)
    with open("styles/" + css_file + ".css") as stylesheet_file:
        stylesheet = stylesheet_file.read()
    if page.head != None:
        new_tag = page.new_tag("style", type="text/css")
        new_tag.string = stylesheet
        page.head.append(new_tag)
    return page


def detectLanguage(page):
    pass
