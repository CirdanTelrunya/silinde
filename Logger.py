#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import time
from datetime import date

class Logger(object):
    def __init__(self):
        self._previous = []
        self._accumulator = []
        self._lastHeader = []
        pass

    def log(self, *item):
        assert len(item) == 2
        self._accumulator.append(item)
        pass
    def display(self):
        for item in self._accumulator:
            print item

    def save(self, file):
        names = ['Training']
        today = date.today()
        values = [today.isoformat()]
        for name, value in self._accumulator:
            names.append(name)
            values.append(value)
        with open(file, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(self._previous)
            if names != self._lastHeader:
                self._lastHeader = names
                writer.writerow(names)
                self._previous.append(names)
            writer.writerow(values)
            self._previous.append(values)
        self._accumulator = []
        pass
    def load(self, file):
        self._previous = []
        self._lastHeader = []
        self._accumulator = []
        
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                self._previous.append(row)
                if row[0] == 'Training':
                    self._lastHeader = row
        pass

if __name__ == "__main__":
    x = Logger()
    x.log('test', 5)
    x.log('test1', 3)
    x.display()
    x.save('/tmp/test.csv')
    x.load('/tmp/test.csv')
    x.log('test', 6)
    x.log('test1', 4)
    x.save('/tmp/test.csv')
    x.load('/tmp/test.csv')
    x.log('test3', 6)
    x.log('test5', 4)    
    x.save('/tmp/test.csv')
    
