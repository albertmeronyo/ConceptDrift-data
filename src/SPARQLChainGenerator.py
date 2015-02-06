#!/usr/bin/env python

# SPARQLChainGenerator.py: Generates versioned datasets out of
# retrieved SPARQL ontologies with owl:priorVersion

import urllib2
import logging
import json
import rdflib
import os
from ConfigParser import SafeConfigParser

CONFIG_INI = "config.ini"

class SPARQLChainGenerator:
    jDump = None

    def __init__(self, __config):
        '''
        Class constructor
        '''
        self.log = logging.getLogger('SPARQLChainGenerator')

        self.config = __config

        self.DS_FILE = self.config.get('general', 'sparql_file')
        self.DS_DIR = self.config.get('general', 'sparql_dir')

        self.initDumpFile()
        self.generateDatasets()

    def initDumpFile(self):
        '''
        Opens dump file
        '''
        f = open(self.DS_FILE, 'r')
        self.jDump = json.load(f)

    def generateDatasets(self):
        '''
        Generates datasets out of URIs in config.ini's dump_file
        '''
        for chain in self.jDump:
            for i,ver in enumerate(chain):
                dirname = ver.split('.')[1]
                uri = ver
                filename = str(i) + "-" + dirname + '.nt'
                filecontent = None
                g = rdflib.Graph()
                try:
                    g.parse(uri)
                except urllib2.HTTPError:
                    self.log.debug("URI not found")
                    pass

                if len(g) > 0:
                    sDir = self.DS_DIR + '/' + dirname
                    sFile = sDir + '/' + filename
                    if not os.path.exists(sDir):
                        os.makedirs(sDir)
                    try:
                        g.serialize(sFile, format='nt')
                    except Exception:
                        self.log.warning("Could not serialize malformed URI, skipping this graph")
                        pass
if __name__ == "__main__":
    # Config
    config = SafeConfigParser()
    config.read(CONFIG_INI)
    
    # Logging
    logLevel = logging.INFO
    if config.get('general', 'verbose') == 1:
        logLevel = logging.DEBUG
    logging.basicConfig(level=logLevel)
    logging.info("Initializing...")

    # Instance
    l = SPARQLChainGenerator(config)
    logging.info("Exiting...")
    exit(0)
