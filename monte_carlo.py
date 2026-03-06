import random

# Global variables
duration_options = [0.0625, 0.125, 0.25, 0.25, 0.5]
NUM_NOTES = 64

# Function to produce rhythms for the melody and harmony 
# depending on a given length
def get_rhythms(length):
    iters = 0
    rhythm_m = make_rand_rhythm()
    while(not is_correct_length(length, rhythm_m)):
        iters += 1
        rhythm_m = make_rand_rhythm()

    rhythm_h = get_rhythm_h(rhythm_m)

    return rhythm_m, rhythm_h

# Generate a random rhythm
def make_rand_rhythm():
    rhythm = []
    for i in range(NUM_NOTES):
        rhythm.append(random.choice(duration_options))
    return rhythm

# Check if a randomo rhythm is the correct length
def is_correct_length(length, rhythm):
    sum = 0.0
    for i in rhythm:
        sum += i
    if sum == length:
        return True
    return False

# Create a harmony rhythm 
def get_rhythm_h(rhythm_m):
    chord_tot = 0
    rhythm_h = []
    for i in range(NUM_NOTES):
        chord_tot += rhythm_m[i]
        if((i % 4) == 3):
            rhythm_h.append(chord_tot)
            chord_tot = 0
    return rhythm_h
