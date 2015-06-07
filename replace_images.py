import re
from wand.image import Image
import urllib
import io
import requests
import os, random
import sys
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless
import StringIO
def getsizes(image_data):
    p = Image.frombytes(image_data)
    return p.image.size

def getImage(width,height):
    return "http://placekitten.com/g/"+str(width)+"/"+str(height)
"""
def parse_image(data):
    page = BeautifulSoup(data)
    #img_regex = re.compile("(<img.*?\/)")
    imgs = page.findAll('img')
    for i in imgs:
        attrs = dict((x,y) for x, y in i.attrs)
        #print(attrs)
        if 'width' in attrs and 'height' in attrs:
            #print(i)
            if int(i['width']) > 40 and int(i['height']) > 40:
                new_attrs = [("src",getImage(i['width'],i['height']))]
                i.attrs = new_attrs
            else:
                sizes = getsizes(i['src'])
                new_attrs = [("src",getImage(sites[1][0],sites[1][1]))]
                i.attrs = new_attrs
                #print(i)
            #print(i)
            im = Image.open("bride.jpg")
    #import pdb; pdb.set_trace()
    return page

if __name__ == "__main__":
    with open("test_data") as data:
        page = parse_image(data.read())
        print(page)"""
def resizeImg(sourceFile, width, height):                                                                                                                                                                                                                                       
    img = Image(filename=sourceFile)
    if width > height:
        img.transform(resize="%d" % (width))
    else:
        img.transform(resize="x%d" % (height))  
    #wd = img.width - width
    #hd = img.height - height
    #import pdb; pdb.set_trace()
    #img.transform(crop=str(width)+"x"+str(height)+"+"+str(wd)+"+"+str(hd))
    img.crop(0,0,width=width, height=height)
    #outerImg.format = img.format.lower()                                                                                                                                                                                                                                                
    #outerImg.composite(img, left=(width - img.width) / 2, top=(img.height-height) / 2)
    img.format = 'jpeg'                                                                                                                                                                                                    
    return img
def replaceImage(flow):
    attrs = dict((x.lower(),y) for x, y in flow.response.headers)
    if "content-type" in attrs:
        if "image" in attrs['content-type'] and not "svg" in attrs['content-type']:
            try:
                if flow.request.code == 200:
                    response = flow.response
                else:
                    response = requests.get(flow.request.url)
            except:
                response = requests.get(flow.request.url)
            try:
                img = Image(file=io.BytesIO(response.content))
                size = img.size
                if size[0] > 80 and size[1] > 80:
                    url = getImage(size[0],size[1])
                    filename = random.choice(os.listdir("images"))
                    img = resizeImg("images/"+filename,size[0],size[1])
                    content = img.make_blob()
                    responseHeaders = ODictCaseless([('Content-Length',len(content))])
                    responseHeaders['Content-Type'] = ["image/jpg"]
                    resp = HTTPResponse([1,1], 200, 'OK', responseHeaders, content)
                    flow.response = resp

            except:
                print(sys.exc_info()[0])
    return flow