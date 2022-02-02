#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import os
import sys


PDFXML = 'wkn1.xml'

def xmlroot(xml):
    return etree.parse(xml).getroot()

root1 = xmlroot(PDFXML)

for page1 in root1.xpath('page'):
    page = {}
    root = page1
    textel_attribs = {}
    textel_text = {}
    for textel in root.iter('text'):
        attributes = {}
        attributes['top'] = int(textel.attrib['top'])
        attributes['left'] = int(textel.attrib['left'])
        attributes['height'] = int(textel.attrib['height'])
        key = (attributes['top'], attributes['left'], attributes['height'])

        textel_attribs[hash(key)] = attributes
        #print(textel_attribs)
        textel_text[hash(key)] = [ txt for txt in textel.itertext() ]


    LEADING = 1
    HORIZONTAL_MARGIN_OF_ERROR = 1
    graph = dict.fromkeys(textel_attribs,[])
#print(textel_attrib)
#sys.exit(1)
    for key in list(textel_attribs.keys()):
        x,y = textel_attribs[key]['left'],textel_attribs[key]['top']
        h = textel_attribs[key]['height']

        vertical_offset = h + LEADING
        min_y = y - vertical_offset
        max_y = y + vertical_offset

        #min_x = x - HORIZONTAL_MARGIN_OF_ERROR
        #max_x = x + HORIZONTAL_MARGIN_OF_ERROR
        min_x = x
        max_x = x
        test_x = x

        tmp_graph_list = []
        
        min_test_attribs = (min_y, test_x, h)
        min_key_test_result = textel_attribs.get(hash(min_test_attribs))
      

        max_test_attribs = (max_y, test_x, h)
        max_key_test_result = textel_attribs.get(hash(max_test_attribs))
       
       
        #if (y,x,h) == (197,111,10):
        #    print(f"this is the key {key}")
        #    print(max_test_attribs)
        #    print(min_test_attribs)
        #    print(f"ktr: {max_key_test_result}")
        if min_key_test_result is not None:
            #print(f"min: {min_test_attribs}")
            if graph[key] == []:
                #print(f"min: {key}: {graph[key]}")
                graph[key] = [hash(min_test_attribs)]
                #print(f"min: {key}: {graph[key]}")
            else:
                graph[key].append(hash(min_test_attribs))

        
        if max_key_test_result is not None:
            if graph[key] == []:
                graph[key] = [hash(max_test_attribs)]
            else:
                graph[key].append(hash(max_test_attribs))
                #print(graph[key])


    for k,v in graph.items():
        if v != []:
            print(f"{k}:{v}")
    sys.exit(1)
    max_len = 0
    maxkey = None
    for key in list(graph.keys()):
        if len(graph[key]) > max_len:
            max_len = len(graph[key])
            maxkey = key

    if maxkey is None:
        pass
    else:
        x,y,z = textel_text[maxkey],textel_text[graph[maxkey][0]],textel_text[graph[maxkey][1]]
        address = [y[0],x[0],z[0]]
        print(address)


