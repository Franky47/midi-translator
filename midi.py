# -*- coding: utf-8 -*-

import rtmidi

# ------------------------------------------------------------------------------

class Midi:
    InvalidType           = 0x00    # For notifying errors
    NoteOff               = 0x80    # Note Off
    NoteOn                = 0x90    # Note On
    AfterTouchPoly        = 0xA0    # Polyphonic AfterTouch
    ControlChange         = 0xB0    # Control Change / Channel Mode
    ProgramChange         = 0xC0    # Program Change
    AfterTouchChannel     = 0xD0    # Channel (monophonic) AfterTouch
    PitchBend             = 0xE0    # Pitch Bend
    SystemExclusive       = 0xF0    # System Exclusive
    TimeCodeQuarterFrame  = 0xF1    # System Common - MIDI Time Code Quarter Frame
    SongPosition          = 0xF2    # System Common - Song Position Pointer
    SongSelect            = 0xF3    # System Common - Song Select
    TuneRequest           = 0xF6    # System Common - Tune Request
    Clock                 = 0xF8    # System Real Time - Timing Clock
    Start                 = 0xFA    # System Real Time - Start
    Continue              = 0xFB    # System Real Time - Continue
    Stop                  = 0xFC    # System Real Time - Stop
    ActiveSensing         = 0xFE    # System Real Time - Active Sensing
    SystemReset           = 0xFF    # System Real Time - System Reset

    @staticmethod
    def getChannel(statusByte):
        return statusByte & 0x0f;

    @staticmethod
    def getType(statusByte):
        if statusByte >= 0xf0:
            # System messages
            return statusByte
        else:
            # Channel messages
            return statusByte & 0xf0;

    class MMC:
        Stop              = 0x01
        Play              = 0x02
        DeferredPlay      = 0x03 # Play when ready
        FastFormward      = 0x04
        Rewind            = 0x05
        RecordStrobe      = 0x06 # Start recording (punch in)
        RecordExit        = 0x07 # Stop recording (punch out)
        RecordPause       = 0x08 # Enter record ready
        Pause             = 0x09
        Eject             = 0x0A
        Chase             = 0x0B
        CommandErrorReset = 0x0C
        MMCReset          = 0x0D

        @staticmethod
        def generate(commandCode, targetId = 0):
            return [0xF0, 0x7F, int(targetId), 0x06, int(commandCode), 0xF7]

# ------------------------------------------------------------------------------

class MidiInterface:
    def __init__(self, listenerCallback = None):
        self.input              = rtmidi.MidiIn()
        self.output             = rtmidi.MidiOut()
        self.listenerCallback   = listenerCallback
        self.ports              = self.getAvailablePorts()
        self.connect(self.choosePorts())

    # --------------------------------------------------------------------------

    class Port:
        def __init__(self, interface, id, name):
            self.interface = interface
            self.virtual   = False
            self.id        = id
            self.name      = name

        @staticmethod
        def createVirtualPort(interface):
            port = MidiInterface.Port(interface, 'v', 'Virtual Port')
            port.virtual = True
            return port

        def open(self):
            if self.virtual:
                self.interface.open_virtual_port()
            else:
                self.interface.open_port(self.id)

        def close(self):
            self.interface.close_port()

    # --------------------------------------------------------------------------

    def handleMidiInput(self, message, timestamp):
        midiData = message[0]
        if self.listenerCallback:
            self.listenerCallback(midiData)

    def send(self, message):
        print('Sending', message)
        self.output.send_message(message)

    # --------------------------------------------------------------------------

    def getAvailablePorts(self):
        inputPorts  = self.input.get_ports()
        outputPorts = self.output.get_ports()
        d = {
            'input' : [MidiInterface.Port.createVirtualPort(self.input)],
            'output': [MidiInterface.Port.createVirtualPort(self.output)],
        }
        for name, id in zip(inputPorts, range(0, len(inputPorts))):
            d['input'].append(MidiInterface.Port(self.input, id, name))
        for name, id in zip(outputPorts, range(0, len(outputPorts))):
            d['output'].append(MidiInterface.Port(self.output, id, name))
        return d

    def choosePorts(self):
        return {
            'input' : self.choosePort(self.ports['input'],  'input'),
            'output': self.choosePort(self.ports['output'], 'output'),
        }

    def choosePort(self, ports, direction):
        print('Select %s port:' % direction)
        choices = { 'x': None }
        print('  [x] No %s' % direction)
        for port in ports:
            print('  [%s]' % str(port.id), port.name)
            choices[str(port.id)] = port
        return choices[input('-> ')]

    # --------------------------------------------------------------------------

    def connect(self, ports):
        assert ports
        assert 'input'  in ports
        assert 'output' in ports

        if not ports['input']:
            pass # No input
        elif ports['input'].virtual:
            print('Creating virtual input port')
            self.input.set_callback(self.handleMidiInput)
            self.input.open_virtual_port()
        else:
            print('Connecting input to %s' % ports['input'].name)
            self.input.set_callback(self.handleMidiInput)
            self.input.open_port(ports['input'].id)

        if not ports['output']:
            pass # No output
        elif ports['output'].virtual:
            print('Creating virtual output port')
            self.output.open_virtual_port()
        else:
            print('Connecting output to %s' % ports['output'].name)
            self.output.open_port(ports['output'].id)
