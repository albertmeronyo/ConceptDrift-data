#!/usr/bin/env python
# -*- coding: utf-8 -*-

# treeDepth.py: compute depth of a RDF Tree

import sys
from rdflib import Graph, URIRef

inFile = sys.argv[1]

def recGraphC(g, h, n, structprop = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")):
    if n not in h:
        h[n] = []
    for s, p, o in g.triples( (None, structprop, n) ):
        if s not in h[n]:
            h[n].append(s)
            recGraphC(g, h, s)

def recGraph(g, h):
    for o in g.objects():
        if isinstance(o, URIRef):
            recGraphC(g, h, o)

def treeDepth(h):
    depths = []
    for root, children in h.iteritems():
        depths.append(treeDepthC(h, root))
    return max(depths)

def treeDepthC(h, n):
    if len(h[n]) == 0:
        return 0
    else:
        for child in h[n]:
            depths = []
            depths.append(treeDepth(h, child))
            return max(depths) + 1

if __name__ == "__main__":
    h = {}
    g = Graph()
    g.parse(inFile, format='nt')
    recGraph(g, h)
    print treeDepth(h)
