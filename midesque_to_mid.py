from midiutil import MIDIFile
import struct
short_list = list()

with open("../../../test.lmg", "rb") as f:
    byte_start = f.read(8)
    byte_end = f.read(8)
    while byte_start:
        unpacked_start = struct.unpack("d", byte_start)[0]
        unpacked_end = struct.unpack("d", byte_end)[0]
        short_list.append([unpacked_start, unpacked_end])
        byte_start = f.read(8)
        byte_end = f.read(8)

print(short_list)

file = MIDIFile(1)
file.addTempo(0,0,120)

time = 0

for time in short_list:
    file.addNote(0, 0, 69, time[0], time[1]-time[0], 127)

with open("myfile.mid", "wb") as open_file:
    file.writeFile(open_file)
