from textgrid import TextGrid
from midiutil import MIDIFile
file = MIDIFile(deinterleave=False)
file.addTempo(0, 0, 60)
x = TextGrid.fromFile("test.TextGrid")
for z in x:
  if z.name == "phone":
    for l in z:
      file.addNote(0, 0, 69, l.minTime, l.duration(), 127)

file.writeFile(open("myfile.mid", "wb"))
