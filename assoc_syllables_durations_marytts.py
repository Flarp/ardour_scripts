from xml.etree.ElementTree import XML
from itertools import chain
from midiutil import MIDIFile
import httplib2
from urllib.parse import urlencode, quote
import sys

text = open(sys.argv[1], "r").read()
print(text)

mary_destination = "http://localhost:59125/process"
allophone_query = urlencode({
  "INPUT_TYPE": "TEXT",
  "INPUT_TEXT": text,
  "LOCALE": "en_US",
  "VOICE": "cmu-slt-hsmm",
  "OUTPUT_TYPE": "ALLOPHONES"
})

durations_query = urlencode({
  "INPUT_TYPE": "TEXT",
  "INPUT_TEXT": text,
  "LOCALE": "en_US",
  "VOICE": "cmu-slt-hsmm",
  "OUTPUT_TYPE": "REALISED_DURATIONS"
})

audio_query = urlencode({
    "INPUT_TYPE": "TEXT",
    "INPUT_TEXT": text,
    "LOCALE": "en_US",
    "VOICE": "cmu-slt-hsmm",
    "OUTPUT_TYPE": "AUDIO",
    "AUDIO": "WAVE"
})

mary_server = httplib2.Http()
(_, allophones_content) = mary_server.request(mary_destination, "POST", allophone_query)
(_, durations_content) = mary_server.request(mary_destination, "POST", durations_query)
(_, audio_content) = mary_server.request(mary_destination, "POST", audio_query)

open("test.wav", "wb").write(audio_content)


SOUND = 0
SILENCE = 1

syllables = list(map(lambda x: x.attrib["ph"].replace(" ",""), XML(allophones_content).findall(".//{http://mary.dfki.de/2002/MaryXML}syllable")))

def temp(x):
  splitted = x.decode().split(" ")
  return [float(splitted[0]), splitted[2]]

durations = list(map(
  temp,
  durations_content.splitlines()[1:]
))

# [position in the syllable list, character position, position in the syllable_duration list]
positions = [0,0,0]
syllable_durations = []
prev_duration = 0

# correct durations
prev_pause = 0
current_shift = 0
prev_time = 0

for i in range(len(durations)):
  durations[i][0] -= current_shift
  if durations[i-1][1] == "_" and ((durations[i][0] - durations[i-1][0]) > 0.2):
    current_shift += prev_time
    durations[i][0] -= prev_time
  prev_time = durations[i][0]

# mark silence and sound
for duration in durations:
  if len(syllable_durations) != (positions[2] + 1):
    syllable_durations.append(["SOUND", 0])
  if duration[1] == "_":
    syllable_durations.append(["SILENCE", duration[0] - prev_duration])
    prev_duration = duration[0]
    positions[2] += 1
    positions[1] = 0
    continue
  positions[1] += len(duration[1])
  syllable_durations[positions[2]][1] += (duration[0] - prev_duration)
  prev_duration = duration[0]
  if positions[1] == len(syllables[positions[0]]):
    positions[0] += 1
    positions[2] += 1
    positions[1] = 0

# write deltas to MIDI file
accum_duration = 0
file = MIDIFile(deinterleave=False)
file.addTempo(0, 0, 60)
for duration in syllable_durations:
  if duration[1] == 0:
    continue
  if duration[0] == "SOUND":
    file.addNote(0, 0, 69, accum_duration, duration[1], 127)
  accum_duration += duration[1]

file.writeFile(open("myfile.mid", "wb"))
