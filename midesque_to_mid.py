from midiutil import MIDIFile
import struct
short_list = list()

with open("../../../test.lmg", "rb") as f:
    bytes = f.read(2)
    while bytes:
        unpacked = struct.unpack("H", bytes)[0]
        short_list.append(unpacked)
        bytes = f.read(2)

print(short_list)

file = MIDIFile(1)
file.addTempo(0,0,120)

time = 0

for time in short_list:
    file.addNote(0, 0, 69, time, 100, 127)

with open("myfile.mid", "wb") as open_file:
    file.writeFile(open_file)
