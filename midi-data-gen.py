#!/usr/bin/env python3

"""MIDI Data Gen

Generate audio data for for training our neural net, using a sound font

Usage:
  midi-data-gen.py <font> <dest>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from pathlib import Path
from datagen.generate import resample_audio, write_midi_file, print_midi_to_audio
import tempfile
import os

def write_output_audio(root_midi_pitch, msduration, fontfile, output_range, dest):

  with tempfile.TemporaryDirectory() as td:

    # make sure the output directory exists
    outdir = os.path.join(dest, "root{}".format(root_midi_pitch), "msec{}".format(msduration))
    Path(outdir).mkdir(parents=True, exist_ok=True)
    midi_file_name = os.path.join(td, "tmp.mid")
    audio_file_name = os.path.join(td, "aud.wav")

    for r in output_range:
      # Compute the ratio of the two speeds
      ratio = (2 ** (1/12)) ** (r - root_midi_pitch)

      # Write the original midi
      write_midi_file(root_midi_pitch, msduration * ratio, midi_file_name)

      # Print the audio
      print_midi_to_audio(midi_file_name, fontfile, audio_file_name)

      # Resample the audio 
      out_file_name = "f{}t{}d{}.wav".format(root_midi_pitch, r, msduration)
      resample_audio(root_midi_pitch, r, audio_file_name, os.path.join(outdir, out_file_name))

    # Finally just write the original
    write_midi_file(root_midi_pitch, msduration, midi_file_name)
    out_file_name = "f{}t{}d{}-truth.wav".format(root_midi_pitch, root_midi_pitch, msduration)
    print_midi_to_audio(midi_file_name, fontfile, os.path.join(outdir, out_file_name))

if __name__ == '__main__':
  arguments = docopt(__doc__, version='MIDI Data Gen 0.1.0')

  rootpath = arguments['<dest>']
  soundfont = arguments['<font>']
  
  # Make the directory to put everything in
  Path(rootpath).mkdir(parents=True, exist_ok=True)

  # Generate the range of input midi pitches
  input_pitches = range(21, 109, 12)

  # Generate the range of durations
  durations = [1000, 2000, 3000]

  # Generate the  minimum and maximum output pitch
  output_range = range(21, 109, 12)

  for p in input_pitches:
    for d in durations:
      print("root: {}, duration {}".format(p, d))
      write_output_audio(p, d, soundfont, output_range, rootpath)
