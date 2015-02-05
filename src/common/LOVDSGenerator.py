#!/usr/bin/env python

# LOVDSGenerator.py: Generates versioned datasets out of
# retrieved LOV verioned vocabularies

import urllib2
import logging
import json
import rdflib
import os

class LOVDSGenerator:
    jDump = None

    def __init__(self, __config):
        '''
        Class constructor
        '''
        self.log = logging.getLogger('LOVDSGenerator')

        self.config = __config

        self.LOV_FILE = self.config.get('general', 'dump_file')
        self.LOV_DIR = self.config.get('general', 'lov_dir')

        self.initDumpFile()
        self.generateDatasets()

    def initDumpFile(self):
        '''
        Opens dump file
        '''
        f = open(self.LOV_FILE, 'r')
        self.jDump = json.load(f)

    def generateDatasets(self):
        '''
        Generates datasets out of URIs in config.ini's dump_file
        '''
        for voc, vers in self.jDump.iteritems():
            if len() >= 3:
                for ver in sorted(vers, key=lambda v: v[0]):
                    dirname = voc
                    uri = ver[1]
                    if len(uri) == 0: 
                        continue
                    filename = ver[0].split(':')[0].split('T')[0] + '-' + voc + '.nt'
                    filecontent = None

                    g = rdflib.Graph()
                    try:
                        g.parse(uri)
                    except urllib2.HTTPError:
                        self.log.debug("URI not found")
                        pass

                    if len(g) > 0:
                        sDir = self.LOV_DIR + '/' + dirname
                        sFile = sDir + '/' + filename
                        if not os.path.exists(sDir):
                            os.makedirs(sDir)
                        try:
                            g.serialize(sFile, format='nt')
                        except Exception:
                            self.log.warning("Could not serialize malformed URI, skipping this graph")
                            pass
