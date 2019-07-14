#!/usr/bin/env python3
import os
import datetime
import json
import subprocess
import re
import multiprocessing
from filelock import FileLock
from collections import namedtuple
from html.parser import HTMLParser

NUMTHREADS=10

face_tuple = namedtuple('Face', ['url', 'mime', 'begin', 'end', 'groupcnt', 'uniqcnt'])

image_re = re.compile(".*mylittlefacewhen.com(:80)?/f/[1-9][0-9]*$")

id_start_re = re.compile(".*mylittlefacewhen.com(:80)?/f/")

tag_re = re.compile(".*http://mylittlefacewhen.com(:80)?/search/\?tag=.*")

with open("mlfw.json") as f:
    r = f.read()


dump = json.loads(r)

try:
    os.mkdir("mlfw_scrape")
except FileExistsError as e:
    pass


class MyHTMLParser(HTMLParser):
    """
    Parser for the html. It searches for the "a" of class "tag" and saves what it finds to an instance variable.
    """
    def __init__(self):
        super().__init__()
        self.last_tag = None
        self.last_attrs = None

    def handle_starttag(self, tag, attrs):
        self.last_tag = tag
        self.last_attr = attrs

    def handle_endtag(self, tag):
        self.last_tag = None
        self.last_attr = None

    def handle_data(self, data):
        if self.last_tag == "a":
            self.last_attr = {k:v for k,v in self.last_attr}
            if "class" in self.last_attr  and self.last_attr["class"] == "tag" and tag_re.match(self.last_attr["href"]):
                self.last_attr = None
                self.last_tag = None
                self.tags.append(data)

    def feed(self, data):
        self.tags = list()
        super().feed(data)
        return self.tags

parser = MyHTMLParser()

def write_error(message):
    with FileLock("/tmp/mlfw_scrape_error.lock"):
        with open("error_log", "a") as error_log:
            print(message, file=error_log)

def extract(workunit):
    idx, face = workunit
    face = face_tuple(*face)
    print ('getting', face)
    url = "https://web.archive.org/web/%(date)s/%(url)s"%dict(date=face.end , url=face.url)
    print(url)
    #download the page
    try:
        o = subprocess.check_output(["curl", url])
    except subprocess.CalledProcessError as e:
        write_error("%s: error on face id %d %s"%(e, idx, face))
        return
    #make a directory for the output and save it
    dir_ = "mlfw_scrape/%s/"%(idx)
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass

    with open(dir_+"foo.html", "wb") as f:
        f.write(o)

    #check to see if it is a face url
    if not image_re.match(face.url):
        print("ignoring", face)
        return
    #parse the html
    o = o.decode("utf-8")
    tags = parser.feed(o)

    return tags

write_error("Run starting %s:"%datetime.datetime.now())
pool = multiprocessing.Pool(NUMTHREADS)
all_tags = pool.map(extract, enumerate(dump[:50]))


tag_mapping = dict()

for idx,tags in enumerate(all_tags):
    face = face_tuple(*dump[idx])
    if tags and image_re.match(face.url):
        id_start = id_start_re.match(face.url).span()[1]
        if not id_start:
            continue

        id_ = face.url[id_start:]
        if id_ in tag_mapping:
            raise KeyError("mlfw id already in mapping")
        
        tag_mapping[id_] = tags


with open("tags.json", "w") as f:
    json.dump(tag_mapping, f)


print(len(tag_mapping), "images' tags extracted")
