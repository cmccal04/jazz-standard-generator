#!/usr/bin/env python3
# Purpose: This program creates a score of music. The melody is created using 
# a markov chain trained by data from the two songs "Autumn Leaves" and 
# "Take Five". The harmony is then generated using a genetic algorithm, 
# where the fitness functin aims to align each chord with a set of 4 notes 
# from the melody. Finally, a monte carlo algorithm is used to generate a
# rythym so that each chord in the harmony lasts the same length as the
# corresponding notes in the melody.
# 
# Author(s): Jeremy Lawrence, Cullen McCaleb
# Date: 10/26/25

import sys
import pickle
from music21 import *
from genetic_alg import get_harmony
from markov_chain import get_melody
from monte_carlo import get_rhythms

NUM_CHUNKS = 16
POPULATION_SIZE = 80
NUM_GENERATIONS = 8

# Save a solution using pickle
def save_solution(data, filename="results/saved_solution.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Load a solution using pickle
def load_solution(filename="results/saved_solution.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)

# Train the algorithms and generate data to build a score
def create_score_data():
    melody = get_melody() # List of streams
    harmony_list = get_harmony(melody, NUM_GENERATIONS, POPULATION_SIZE) # List of lists
    rhythm_m, rhythm_h = get_rhythms(NUM_CHUNKS) # List of floats

    data = {
        "melody": melody,
        "harmony_list": harmony_list,
        "rhythm_m": rhythm_m,
        "rhythm_h": rhythm_h,
    }
    return data
    
# Build the score based off given data, which holds the melody, harmony, 
# and rhythms
def build_score(data):
    melody = data["melody"]
    harmony_list = data["harmony_list"]
    rhythm_m = data["rhythm_m"]
    rhythm_h = data["rhythm_h"]

    top_level_m = stream.Part()
    top_level_h = stream.Part()

    harmony = stream.Part()
    bass = clef.BassClef()
    harmony.append(bass)

    melody_pitches = []
    for i, s in enumerate(melody):
        for p in s.pitches:
            melody_pitches.append(p)
        
        new_chord = chord.Chord(harmony_list[i])
        dur = duration.Duration(quarterLength=rhythm_h[i] * 4)
        new_chord.duration = dur
        top_level_h.append(new_chord)
    
    for i, r in enumerate(rhythm_m):
        new_note = note.Note(melody_pitches[i])
        dur = duration.Duration(quarterLength=r * 4)
        new_note.duration = dur
        top_level_m.append(new_note)
    
    top_level = stream.Score()
    
    top_level.insert(0, top_level_m)
    top_level.insert(0, top_level_h)

    return top_level

# Main function to either build the score oor load it from saved_solution.pkl, 
# depending on the arguments. Then, create a .xml or .midi file depending on 
# the arguments.
def main():
    if("--train" in sys.argv):
        data = create_score_data()
        save_solution(data)
    elif("--use" in sys.argv):
        data = load_solution()
    else:
        data = create_score_data()
    
    top_level = build_score(data)

    # Play midi, output sheet music, or print the contents of the stream
    if ("-m" in sys.argv):
        top_level.write('midi', fp="results/out.midi")
    elif ("-s" in sys.argv):
        top_level.write(fp="results/out.xml")
    else:
        top_level.show('text') #Useful for debugging!

if __name__ == "__main__":
    main()
