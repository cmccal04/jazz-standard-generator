# Jazz Standard Generator

**Authors:** Cullen McCaleb and Jeremy Lawrence

---

## Files

| File | Description |
|------|-------------|
| `generator.py` | Main file that creates the composition |
| `markov_chain.py` | Provides functions to create a Markov chain-based melody part |
| `genetic_algorithm.py` | Provides functions to create a genetic algorithm-based harmony part |
| `monte_carlo.py` | Provides a function to generate note durations for a melody and harmony part |
| `results` | Sotres MIDI files adn XML files used by `generator.py` |
| `standards` | Stores MIDI files used by `markov_chain.py` which act as inspiration for the algorithm |

---

## Usage

```bash
python3 generator.py [ -s | -m ] [ --train | --use ]
```

- `-s` or `-m` is required: `-s` creates an xml file for the score, and `-m` creates a midi file
- `--train` or `--use` are optional: the default is training mode

---

## Composition Description

This composition combines the genetic algorithm, Markov chain, and Monte Carlo method approaches to generate an original piece based on two Jazz standards: *Autumn Leaves* and *Take Five*.

- **Markov Chain:** Attempts to combine the melody and solo parts of both songs, ignoring rhythm entirely. The transition matrix is computed empirically from note counts in each song, and the melody is determined by the transition probabilities of the previous pitch. The melody is divided into chunks of four notes.

- **Genetic Algorithm:** Generates one chord for each 4-note melody chunk. Each chromosome consists of all the chords for the piece in a list, where chords are lists of 3 notes. The fitness function evaluates the chromosome based on how many notes are in the key of the corresponding four melody notes.

- **Monte Carlo:** Generates random rhythm combinations and selects a solution that results in the melody and harmony being the same length.

---

## Visualization

Because the melody is based on other songs, the composition contains motifs from the originals. For example, a descending chromatic line from *Take Five* is reproduced by the Markov chain due to its frequent appearance in that song. Note that enharmonic spelling is not always preserved, likely due to how MuseScore4 and Music21 process and transpose pitches.

In one example 4-note melody chunk (E, F, G, C), every pitch belongs to the C major and F major scales. The generated chord contains pitches D, A#, and F. Since Bb and A# are enharmonically equivalent, the chord sounds like a Bb major triad — diatonic to the F major scale — and thus receives a high fitness score.

---

## Reflection

- Finding Jazz songs with easily extractable melodies, and locating suitable MIDI files, was one of the most time-consuming parts of the project.
- Designing efficient crossover and mutation operators for the genetic algorithm was challenging; the current implementation does a poor job of maintaining good solutions across generations.
- The genetic algorithm could be made significantly more efficient — the final composition took **24 minutes** to generate.
