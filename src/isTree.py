#!/usr/bin/env python
# -*- coding: utf-8 -*-

# isTree.py: check if RDF graph is a tree

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


def isTree(h):
    for root, children in h.iteritems():
        if not isTreeC(h, root):
            return False
    return True

def isTreeC(h, n):
    visited = []
    stack = []
    stack.append(n)
    while stack:
        currElem = stack.pop()
        if currElem in visited:
            return False
        visited.append(currElem)
        for child in h[currElem]:
            stack.append(child)
    return True

if __name__ == "__main__":
    h = {}
    g = Graph()
    g.parse(inFile, format='nt')
    recGraph(g, h)
    print isTree(h)
