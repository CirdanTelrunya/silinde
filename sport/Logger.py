#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

class Logger(object):
    def __init__(self):
        self._accumulator = []
        pass

    def log(self, *item):
        self._accumulator.append(item)
        pass
    def display(self):
        for item in self._accumulator:
            print item

    def save(self, file):
        names = []
        values = []
        for name, value in self._accumulator:
            names.append(name)
            values.append(value)
        with open(file, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(names)
            writer.writerow(values)
        pass
if __name__ == "__main__":
    x = Logger()
    x.log('test', 5)
    x.log('test1', 3)
    x.display()
    x.save('/tmp/test.csv')
