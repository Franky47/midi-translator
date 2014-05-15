# -*- coding: utf-8 -*-

from midi       import Midi, MidiInterface
from engine     import Engine, TranslationUnit, Thru

# ------------------------------------------------------------------------------

def populate(engine):
    # Logidy UMI3 -> Pro Tools (MMC Slave)
    engine.translationUnits.append(TranslationUnit([Midi.Start],    Midi.MMC.generate(Midi.MMC.Play, 127)))
    engine.translationUnits.append(TranslationUnit([Midi.Stop],     Midi.MMC.generate(Midi.MMC.Stop, 127)))
    engine.translationUnits.append(TranslationUnit([Midi.Continue], Midi.MMC.generate(Midi.MMC.RecordStrobe, 127)))
    engine.translationUnits.append(Thru())

# ------------------------------------------------------------------------------

def main():
    midiInterface = MidiInterface()
    engine = Engine(midiInterface)
    populate(engine)
    midiInterface.listenerCallback = engine.handleMidiInput

    while True:
        # Loop until quitting
        pass

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
