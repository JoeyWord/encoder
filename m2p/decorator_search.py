#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   decorator_search.py
@Time    :   2019/07/25 22:05:13
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from lxml import objectify
from lxml.etree import XML
from lxml.objectify import ObjectifiedElement
from wrapt import decorator
from wrap import test_decorator4




class Outer():
    ancestor = "//movie"
    def __init__(self):
        pass
    
    @test_decorator4(ancestor,"obj")
    def extractor(self,obj,nsmap):
        guid_xpath = obj.xpath(".//description",namespaces=nsmap)
        if guid_xpath:
            text = guid_xpath[0].xpath("./text()",namespaces=nsmap)
            span_attr = guid_xpath[0].xpath("./span",namespaces=nsmap)
            names = []
            for _span in span_attr:
                names.append(_span.attrib.get("name"))
            return text,names
        return

if __name__ == "__main__":
    with open("file\\test.xml","r",encoding="utf-8") as fr:
        xml_doc = fr.read()
    xml_obj = XML(xml_doc.encode("utf-8"))
    nsmap = xml_obj.nsmap
    # nsmap = {}
    print("namespace:",nsmap)
    out = Outer()
    xml = objectify.fromstring(xml_doc)
    # print("type of xml:",type(xml))
    # nodes = xml.xpath("//movie[@title='Transformers']",namespaces=nsmap)
    # if nodes:
    #     print(type(nodes[0]))
    res = out.extractor(xml,nsmap)
    if res:
        print("name sign:",out.extractor.__name__)
        print("text={} and names={}".format(*res))
