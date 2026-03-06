from music21 import *
import numpy as np
import random

# Creates a list of streams, each representing a melody chunk,
# given the chunk size and number of chunks.
def get_melody(chunk_size=4, num_chunks=16):
    take5 = converter.parse('standards/Take5.mid')
    autumn = converter.parse('standards/AutumnLeaves.mid')
    all_notes = []

    # Extract melody and solo parts from "Take Five"
    for i, part in enumerate(take5.parts):
        if i in [3, 8, 9]:
            part.transpose(2, inPlace=True)
            all_notes.append(encode_part(part))
            all_notes.append(encode_part(part))

    # Extract melody and solo parts from "Autumn Leaves"
    for part in autumn.parts:
        part.transpose(3, inPlace=True)
        if "Melody" in part.partName or "Solo" in part.partName:
            all_notes.append(encode_part(part))
    
    transition_matrix, pitch_map = markov_chain(all_notes)
    melody = generate_melody(transition_matrix, chunk_size * num_chunks, pitch_map)

    # Convert the melody (list of pitch lists) to a list of streams
    melody_chunks = []
    for i in range(num_chunks):
        chunk = stream.Stream()
        for j in range(chunk_size):
            new_note = note.Note(melody[chunk_size * i + j])
            chunk.append(new_note)
        melody_chunks.append(chunk)
    
    return melody_chunks

# Creates a list of Music21 pitches, given a Music21 part.
# Breaks chords into individual pitches, which is necessary when
# Music21 converter incorrectly parses triplet 16th notes as chords.
def encode_part(part):
    pitches = []
    for element in part.flatten().notesAndRests:
        if isinstance(element, note.Note):
            pitches.append(element.pitch)

        # Break chords into individual pitches
        elif isinstance(element, chord.Chord):
            for pitch in element.pitches:
                pitches.append(pitch)
    return pitches

# Builds a 1st order Markov Chain based on a list of Music21 parts,
# as well as a dictionary from pitch to index in the matrix
def markov_chain(parts):
    flat_list = [pitch for part in parts for pitch in part]
    unique_pitches = list(dict.fromkeys(flat_list))
    n = len(unique_pitches)

    pitch_to_idx = {pitch: i for i, pitch in enumerate(unique_pitches)}
    idx_to_pitch = {i: p for p, i in pitch_to_idx.items()}

    # Count the frequency of each pitch transition in each part.
    # Each part is processed separately to avoid artificial
    # transitions between distinct parts.
    transition_matrix = np.zeros((n, n))
    for part in parts:
        for p1, p2 in zip(part, part[1:]):
            curr_idx = pitch_to_idx[p1]
            next_idx = pitch_to_idx[p2]
            transition_matrix[curr_idx, next_idx] += 1
    
    # Transform matrix into an array of probability vectors
    for i in range(n):
        row_sum = np.sum(transition_matrix[i], keepdims=True)
        if row_sum > 0:
            transition_matrix[i] /= row_sum
        # To avoid early termination, add transitions to 0-rows
        else:
            transition_matrix[i] = np.full(n, 1 / n)

    return transition_matrix, idx_to_pitch

# Generates a list of Music21 pitches from a Markov Chain, given a melody
# length, index-to-pitch dictionary, and an optional starting note index
def generate_melody(matrix, length, idx_to_pitch, start=None):
    # Choose random starting note if none is given
    if start is None:
        curr = random.randrange(matrix.shape[0])
    else:
        curr = start
    indices = [curr]

    # Choose the next note based on transition probabilities
    for _ in range(length - 1):
        prob_row = matrix[curr]
        cumulative_probs = np.cumsum(prob_row)
        r = random.random()
        curr = np.argmax(cumulative_probs > r)
        indices.append(curr)
    
    return [idx_to_pitch[i] for i in indices]
