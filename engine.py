# -*- coding: utf-8 -*-

import sys

# ------------------------------------------------------------------------------

class Engine:
    def __init__(self, interface):
        self.interface = interface
        self.translationUnits = []

    def handleMidiInput(self, data):
        for t in self.translationUnits:
            processed = t.process(data)
            if processed:
                self.interface.send(processed)

# ------------------------------------------------------------------------------

class TranslationUnit:
    def __init__(self, input, output):
        self.input  = input
        self.output = output

    def process(self, data):
        return self.output if self.input == data else None

# ------------------------------------------------------------------------------

if sys.version >= '3.0':

    class Thru(TranslationUnit):
        def __init__(self):
            super().__init__(None, None)

        def process(self, data):
            return data

else:

    class Thru(TranslationUnit):
        def __init__(self):
            TranslationUnit.__init__(self, None, None)

        def process(self, data):
            return data
