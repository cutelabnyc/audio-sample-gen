
from midiutil import MIDIFile
import subprocess
import mutagen
import ffmpeg
import pdb

def write_midi_file(pitch, msduration, dest, velocity=100):
    
    mid = MIDIFile(1)
    tempo = 60000 / msduration
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    volume   = velocity

    mid.addTempo(track, time, tempo)
    mid.addNote(track, channel, pitch, time, duration, volume)
    with open(dest, "wb") as output_file:
        mid.writeFile(output_file)

def print_midi_to_audio(inmidi, soundfont, dest):
    exec_print = subprocess.run(["fluidsynth", soundfont, inmidi, "-F", dest])

def resample_audio(inmidipitch, outmidipitch, infile, outfile):
    # For now assume 44100
    ratio = (2 ** (1/12)) ** (outmidipitch - inmidipitch)
    out_sr = int(ratio * 44100)
    exec_resample = subprocess.run(["ffmpeg", "-i", infile, "-af", "asetrate=r={}".format(out_sr), outfile])