from xml.etree.ElementTree import parse
from itertools import chain

# my year of haskell has culmuinated into this one blob of code
syllables = list(
    chain(
      *map(lambda prosody: list(
        map(
          lambda x: x.attrib["ph"].replace(" ", ""),
          prosody[0].iter("{http://mary.dfki.de/2002/MaryXML}syllable")
        )
      )
    , parse("allophones.xml").getroot()[0][0])
  )
)

def temp(x):
  splitted = x.split(" ")
  return [float(splitted[0]), splitted[2]]

durations = list(map(
  temp,
  open("durations.txt").read().splitlines()[1:]
))

print(durations)
