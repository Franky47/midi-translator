# -*- coding: utf-8 -*-

import sys
import os
import shutil
import subprocess
from pprint     import pprint
from midi       import *
from tester     import *

# ------------------------------------------------------------------------------

def main():
    midiInterface = MidiInterface()
    #tester  = Tester(midiInterface)
    #midiInterface.listenerCallback = tester.handleMidiInput

    while True:
        midiInterface.send(Midi.MMC.generate(Midi.MMC.Play))



# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
