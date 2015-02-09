#!/usr/bin/env python

# dataAnalysis.py: correlation analysis between version chain
# features and performance of OEML

import csv
import os
import logging
from rdflib import Graph
from ConfigParser import SafeConfigParser

CONFIG_INI = "config.ini"

class DataAnalysis:

    def __init__(self, __config):
        '''
        Class constructor
        '''
        self.log = logging.getLogger('DataAnalysis')

        self.config = __config
        self.stats = []
        self.PATHS = self.config.get('analysis', 'analysis_dir')
        self.PATHS = self.PATHS.split(',')
        self.OUT_FILE = self.config.get('analysis', 'stats_out_file')

        self.log.info("Starting tasks...")
        self.log.info("Parsing all data dirs...")
        self.runAnalysisDirs(self.PATHS)
        self.log.info("Serializing results...")
        self.serializeAnalysis()
        self.log.info("All done.")

    def runAnalysisDirs(self, paths):
        '''
        Runs the analysis of all datasets under the indicated PATH
        '''
        for path in paths:
            for root,subdirs,files in os.walk(path):
                self.currRoot = root
                if subdirs:
                    self.runAnalysisDirs(subdirs)
                self.runAnalysis(files)
            
    def runAnalysis(self, fs):
        '''
        Runs the analysis on one file
        '''
        self.log.info("Analysing dataset %s" % os.path.join(self.currRoot))
        dataset = os.path.join(self.currRoot)
        size = 10
        isTree = False
        for f in fs:
            g = Graph()
            # g.parse(f, format='nt')
            # self.log.info(len(g))
        self.stats.append([dataset, size, isTree])

    def serializeAnalysis(self):
        '''
        Serializes analysis results to OUT_FILE
        '''
        with open(self.OUT_FILE, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.config.get('analysis', 'headers').split(','))
            for row in self.stats:
                writer.writerow(row)

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
    l = DataAnalysis(config)
    logging.info("Exiting...")
    exit(0)
