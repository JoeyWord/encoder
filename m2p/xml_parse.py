# coding=utf-8

from xml.sax import ContentHandler,make_parser,handler
from xml.dom.minidom import parse,parseString
import os
import traceback

#way1 by sax belong the transction deal,which can cost less cpu and memory
class SaxParse(ContentHandler):
    def __init__(self):
        self.title = ""
        self.type = ""
        self.types = []
        self.format = ""
        self.formats = []
        self.rating = ""
        self.ratings = []
        self.content = ""
    
    def startElement(self,tag,attrs):
        self.content = tag
        if tag == "movie":
            print("\n*****movie info*****")
            title = attrs.get("title")
            print("title of movie:{}".format(title))
    
    def endElement(self,tag):
        if self.content == "type":
            print("type result: %s" %self.type)
            self.types.append(self.type)
        elif self.content == "format":
            print("format result: %s" %self.format)
        elif tag== "rating":
            print("rating result: %s" %self.rating)
        self.content = ""
    
    def characters(self,content):
        if self.content == "type":
            self.type = content
        elif self.content == "format":
            self.format = content
        elif self.content == "rating":
            self.rating = content

def parse_by_dom(xml_file,tag):
    doc_tree = parseString(open(xml_file,'r').read()).documentElement
    movies = doc_tree.getElementsByTagName("movie")
    print("movies info:",movies)
    for movie in movies:
        if movie.hasAttribute("title"):
            print("\n\n*****movie title*****")
            title = movie.getAttribute("title")
            print("title info: %s" %title)
            tags = movie.getElementsByTagName(tag)
            if tags:
                print("tag %s info is: %s" %(tag,tags[0].childNodes[0].data))

def parse_by_etree(xml_file,tag):
    from xml.etree import ElementTree
    with open(xml_file,'r') as fr:
        tree = ElementTree.fromstring(fr.read())
    print("tree tag={} and tree text={} and tree attrib={}".format(tree.tag,tree.text,tree.attrib))
    #find movie
    movies = tree.findall("movie")
    for movie in movies:
        print("*****moive title begain*****")
        if "title" in movie.attrib:
            print("title info: %s" %movie.attrib.get("title"))
        tag_ = movie.find(tag)
        if tag_:
            print("tag %s info: %s" %(tag_,tag_.text))

if __name__ == "__main__":
    print "doudou"
    saxParse = SaxParse()
    # create sax parser
    parser = make_parser()
    # close namespace
    parser.setFeature(handler.feature_namespaces,0)
    # add handle to parse
    parser.setContentHandler(saxParse)
    # analysis xml doc
    parser.parse(os.path.join("file","test.xml"))
    print("saxParse types: ",saxParse.types)

    parse_by_dom(os.path.join("file","test.xml"),"type")
    parse_by_etree(os.path.join("file","test.xml"),"type")

