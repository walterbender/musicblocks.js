# -*- coding: utf-8 -*-

# Copyright (c) 2020, 2021 Walter Bender, Sugar Labs
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the The GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import math

SHARP = "♯"
FLAT = "♭"
NATURAL = "♮"
DOUBLESHARP = "𝄪"
DOUBLEFLAT = "𝄫"


def normalize_pitch(pitch):
    """
    Internally, we use a standardize form for our pitch letter names:
    * Lowercase c, d, e, f, g, a, b for letter names;
    * #, b, x, and bb for sharp, flat, double sharp, and double flat for
      accidentals.

    Note names for temperaments with more than 12 semitones are of the
    form: n0, n1, ...

    Parameters
    ----------
    pitch : str
        Upper or lowecase pitch name with accidentals as ascii or unicode

    Returns
    -------
    str
        Normalized pitch name
    """
    if type(pitch) == int:
        return pitch
    elif type(pitch) == float:
        return pitch
    pitch = pitch.lower()
    pitch = pitch.replace(SHARP, "#")
    pitch = pitch.replace(DOUBLESHARP, "x")
    pitch = pitch.replace(FLAT, "b")
    pitch = pitch.replace(DOUBLEFLAT, "bb")
    pitch = pitch.replace(NATURAL, "")
    return pitch


def display_pitch(pitch):
    """
    The internal pitch name is converted to unicode, e.g., cb --> C♭

    Parameters
    ----------
    pitch : str
        Upper or lowecase pitch name with accidentals as ascii or unicode

    Returns
    -------
    str
        Pretty pitch name
    """
    # Ignore pitch numbers and pitch expressed as Hertz
    if type(pitch) == int:
        return pitch
    elif type(pitch) == float:
        return pitch
    display_pitch = pitch[0].upper()
    if len(pitch) > 2 and pitch[1:2] == "bb":
        display_pitch += DOUBLEFLAT
    elif len(pitch) > 1:
        if "#" == pitch[1]:
            display_pitch += SHARP
        elif "x" == pitch[1].lower():
            display_pitch += DOUBLESHARP
        elif "b" == pitch[1].lower():
            display_pitch += FLAT
    return display_pitch


class Temperament:
    """
    In musical tuning, temperament is a tuning system that defines the
    notes (semitones) in an octave. Most modern Western musical
    instruments are tuned in the equal temperament system based on the
    1/12 root of 2 (12 semitones per octave). Many traditional
    temperaments are based on ratios.
    """

    # The intervals define which ratios are used to define the notes
    # within a given temperament.
    default_intervals = [
        "perfect 1",
        "minor 2",
        "major 2",
        "minor 3",
        "major 3",
        "perfect 4",
        "diminished 5",
        "perfect 5",
        "minor 6",
        "major 6",
        "minor 7",
        "major 7",
        "perfect 8",
    ]

    twelve_tone_equal_ratios = {
        "perfect 1": 1,
        "minor 2": math.pow(2, 1 / 12),
        "augmented 1": math.pow(2, 1 / 12),
        "major 2": math.pow(2, 2 / 12),
        "augmented 2": math.pow(2, 3 / 12),
        "minor 3": math.pow(2, 3 / 12),
        "major 3": math.pow(2, 4 / 12),
        "augmented 3": math.pow(2, 5 / 12),
        "diminished 4": math.pow(2, 4 / 12),
        "perfect 4": math.pow(2, 5 / 12),
        "augmented 4": math.pow(2, 6 / 12),
        "diminished 5": math.pow(2, 6 / 12),
        "perfect 5": math.pow(2, 7 / 12),
        "augmented 5": math.pow(2, 8 / 12),
        "minor 6": math.pow(2, 8 / 12),
        "major 6": math.pow(2, 9 / 12),
        "augmented 6": math.pow(2, 10 / 12),
        "minor 7": math.pow(2, 10 / 12),
        "major 7": math.pow(2, 11 / 12),
        "augmented 7": math.pow(2, 12 / 12),
        "diminished 8": math.pow(2, 11 / 12),
        "perfect 8": 2,
    }

    just_intonation_ratios = {
        "perfect 1": 1,
        "minor 2": 16 / 15,
        "augmented 1": 16 / 15,
        "major 2": 9 / 8,
        "augmented 2": 6 / 5,
        "minor 3": 6 / 5,
        "major 3": 5 / 4,
        "augmented 3": 4 / 3,
        "diminished 4": 5 / 4,
        "perfect 4": 4 / 3,
        "augmented 4": 7 / 5,
        "diminished 5": 7 / 5,
        "perfect 5": 3 / 2,
        "augmented 5": 8 / 5,
        "minor 6": 8 / 5,
        "major 6": 5 / 3,
        "augmented 6": 16 / 9,
        "minor 7": 16 / 9,
        "major 7": 15 / 8,
        "augmented 7": 2 / 1,
        "diminished 8": 15 / 8,
        "perfect 8": 2,
    }

    pythagorean_ratios = {
        "perfect 1": 1,
        "minor 2": 256 / 243,
        "augmented 1": 256 / 243,
        "major 2": 9 / 8,
        "augmented 2": 32 / 27,
        "minor 3": 32 / 27,
        "major 3": 81 / 64,
        "augmented 3": 4 / 3,
        "diminished 4": 81 / 64,
        "perfect 4": 4 / 3,
        "augmented 4": 729 / 512,
        "diminished 5": 729 / 512,
        "perfect 5": 3 / 2,
        "augmented 5": 128 / 81,
        "minor 6": 128 / 81,
        "major 6": 27 / 16,
        "augmented 6": 16 / 9,
        "minor 7": 16 / 9,
        "major 7": 243 / 128,
        "augmented 7": 2 / 1,
        "diminished 8": 243 / 128,
        "perfect 8": 2,
    }

    third_comma_meantone_ratios = {
        "perfect 1": 1,
        "minor 2": 1.075693,
        "augmented 1": 1.037156,
        "major 2": 1.115656,
        "augmented 2": 1.157109,
        "minor 3": 1.200103,
        "major 3": 1.244694,
        "augmented 3": 1.290943,
        "diminished 4": 1.290943,
        "perfect 4": 1.338902,
        "augmented 4": 1.38865,
        "diminished 5": 1.440247,
        "perfect 5": 1.493762,
        "augmented 5": 1.549255,
        "minor 6": 1.60682,
        "major 6": 1.666524,
        "augmented 6": 1.728445,
        "minor 7": 1.792668,
        "major 7": 1.859266,
        "augmented 7": 1.92835,
        "diminished 8": 1.92835,
        "perfect 8": 2,
    }

    third_comma_meantone_intervals = [
        "perfect 1",
        "augmented 1",
        "minor 2",
        "major 2",
        "augmented 2",
        "minor 3",
        "major 3",
        "diminished 4",
        "perfect 4",
        "augmented 4",
        "diminished 5",
        "perfect 5",
        "augmented 5",
        "minor 6",
        "major 6",
        "augmented 6",
        "minor 7",
        "major 7",
        "diminished 8",
        "perfect 8",
    ]

    quarter_comma_meantone_ratios = {
        "perfect 1": 1,
        "minor 2": 16 / 15,
        "augmented 1": 25 / 24,
        "major 2": 9 / 8,
        "augmented 2": 75 / 64,
        "minor 3": 6 / 5,
        "major 3": 5 / 4,
        "diminished 4": 32 / 25,
        "augmented 3": 125 / 96,
        "perfect 4": 4 / 3,
        "augmented 4": 25 / 18,
        "diminished 5": 36 / 25,
        "perfect 5": 3 / 2,
        "augmented 5": 25 / 16,
        "minor 6": 8 / 5,
        "major 6": 5 / 3,
        "augmented 6": 125 / 72,
        "minor 7": 9 / 5,
        "major 7": 15 / 8,
        "diminished 8": 48 / 25,
        "augmented 7": 125 / 64,
        "perfect 8": 2,
    }

    quarter_comma_meantone_intervals = [
        "perfect 1",
        "augmented 1",
        "minor 2",
        "major 2",
        "augmented 2",
        "minor 3",
        "major 3",
        "diminished 4",
        "augmented 3",
        "perfect 4",
        "augmented 4",
        "diminished 5",
        "perfect 5",
        "augmented 5",
        "minor 6",
        "major 6",
        "augmented 6",
        "minor 7",
        "major 7",
        "diminished 8",
        "augmented 7",
        "perfect 8",
    ]

    freqs = []  # Each temperament contains a list of notes in hertz.
    generic_note_names = []  # An array of names for each note in an octave
    C0 = 16.353  # By default, we use C in Octave 0 as our base frequency.

    def __init__(self, name="equal"):
        """
        Initialize the class. A temperament will be generated but it can
        subsequently be overriden.

        Parameters
        ----------

        name : str
            The name of a temperament, e.g., "equal", "just intonation". etc.

        """
        self.name = name
        self.octave_length = 12  # in semitones
        self.base_frequency = self.C0
        self.number_of_octaves = 8
        self.generate(self.name)

    def set_base_frequency(self, base_frequency):
        """
        The base frequency is used as the starting point for generating
        the notes.

        Parameters
        ----------
        base_frequency : float
            The frequency (in Hertz) used to seed the calculation of the
            notes used in the temperament.
        """
        self.base_frequency = base_frequency

    def get_base_frequency(self):
        """
        Returns
        -------
        float
            The base frequency (in Hertz) used to seed the calculations
        """
        return self.base_frequency

    def set_number_of_octaves(self, number_of_octaves=8):
        """
        How many octaves are defined for the temperament?

        Parameters
        ----------
        number_of_octaves : int
            The number of octaves in the temperament. (8 octaves in
            equal temperament would span 96 notes).
        """
        self.number_of_octaves = min(1, int(abs(number_of_octaves)))

    def get_number_of_octaves(self):
        """
        Returns
        -------
        int
            The number of octaves in the temperament.
        """
        return self.number_of_octaves

    def get_name(self):
        """
        Returns
        -------
        str
            The name of the temperament
        """
        return self.name

    def get_freqs(self):
        """
        freqs is the list of all of the frequencies in the temperament. 

        Returns
        -------
        list
            A list of frequencies in Hertz (float)
        """
        return self.freqs

    def get_note_names(self):
        """
        Generic note names are assigned to define a chromatic scale.

        Returns
        -------
        list
            A list of note names (str)
        """
        return self.generic_note_names

    def get_freq_by_index(self, pitch_index):
        """
        Parameters
        ----------
        pitch_index : int
            The index into the frequency list

        Returns
        -------
        float
            Returns the frequency (in Hertz) of a note by index
        """
        if len(self.freqs) == 0:
            return 0
        if pitch_index < 0:
            pitch_index = 0
        if pitch_index > len(self.freqs) - 1:
            pitch_index = len(self.freqs) - 1
        return self.freqs[int(pitch_index)]

    def get_freq_by_modal_index_and_octave(self, modal_index, octave):
        """
        Modal index is an index into the notes in a octave.

        Parameters
        ----------
        modal_index : int
            The index of the note within an octave

        octave : int
            Which octave to access

        Returns
        -------
        float
            The frequency that corresponds to the index and octave (in Hertz)
        """
        if len(self.freqs) == 0:
            return 0
        i = (int(octave) * self.octave_length) + modal_index
        if i < 0:
            return self.freqs[0]
        if i > len(self.freqs) - 1:
            return self.freqs[-1]
        return self.freqs[int(i)]

    def get_freq_by_generic_note_name_and_octave(self, note_name, octave):
        """
        Note name can be used to calculate an index the notes in an octave.

        Parameters
        ----------
        note_name : str
            The name of the note

        octave : int
            Which octave to access

        Returns
        -------
        float
            The frequency that corresponds to the index and octave (in Hertz)
        """
        if len(self.freqs) == 0:
            return 0
        if note_name not in self.generic_note_names:
            print("Note %s not found in generic note names." % (note_name))
            return 0
        ni = self.generic_note_names.index(note_name)
        i = (octave * self.octave_length) + ni
        if i < 0:
            return self.freqs[0]
        if i > len(self.freqs) - 1:
            return self.freqs[-1]
        return self.freqs[int(i)]

    def get_number_of_semitones_in_octave(self):
        """
        Returns
        -------
        int
            The number of notes defined per octave
        """
        return self.octave_length

    def generate_generic_note_names(self):
        """
        A generic name is defined for each note in the octave.
        The convention is n0, n1, etc. These notes can be used by
        the get_freq_by_generic_note_name_and_octave method to retrieve
        a frequency by note name and octave.
        """
        self.generic_note_names = []
        for i in range(self.octave_length):
            self.generic_note_names.append("n%d" % i)

    def generate(self, name):
        """
        Generate creates one of the predefined temperaments based on the
        rules for generating the frequencies and the selected intervals used
        to determine which frequencies to include in the temperament.
        A rule might be to use a series of ratios between steps, as in the
        Pythagorean temperament, or to use a fixed ratio, such as the
        twelth root of two when calculating equal temperament.

        The base frequency used when applying the rules is defined in
        self.base_frequency
        The number of times to apply the rules is determined by
        self.number_of_octaves
        The resultant frequencies are stored in self.freqs
        The resultant number of notes per octave is stored in
        self.octave_length

        Parameters
        ----------
        name : str
            The name of one of the predefined temperaments
        """
        self.name = name.lower()

        if self.name == "third comma meantone":
            intervals = self.third_comma_meantone_intervals[:]
            ratios = self.third_comma_meantone_ratios
        elif self.name == "quarter comma meantone":
            intervals = self.quarter_comma_meantone_intervals[:]
            ratios = self.quarter_comma_meantone_ratios
        else:
            intervals = self.default_intervals[:]
            if self.name == "equal":
                ratios = self.twelve_tone_equal_ratios
            elif self.name == "just intonation":
                ratios = self.just_intonation_ratios
            elif self.name == "pythagorean":
                ratios = self.pythagorean_ratios
            else:
                print("Unknown temperament %d; using equal temperament" % (name))
                ratios = self.twelve_tone_equal_ratios

        self.octave_length = len(intervals) - 1
        self.freqs = [self.base_frequency]

        for octave in range(self.number_of_octaves):
            c = self.freqs[-1]
            for i in range(self.octave_length):
                if i == 0:
                    continue
                self.freqs.append(c * ratios[intervals[i]])

        self.generate_generic_note_names()

    def generate_equal_temperament(self, number_of_steps):
        """
        Equal temperaments can be generated for different numbers of steps
        between the notes in an octave. The predefined equal temperament
        defines 12 steps per octave, which is perhaps the most common
        tuning system in modern Western music. But any number of steps can
        be used.

        Parameters
        ----------
        number_of_steps : int
            The number of equal steps into which to divide an octave.
        """
        nsteps = int(number_of_steps)
        if nsteps < 1:
            nsteps = 1

        self.name = "name_%d" % nsteps

        self.octave_length = nsteps
        self.freqs = [self.base_frequency]

        # nth root of 2
        root = 2 ** (1 / nsteps)
        for octave in range(self.number_of_octaves):
            for i in range(self.octave_length):
                if i == 0:
                    continue
                self.freqs.append(self.freqs[-1] * root)

        self.generate_generic_note_names()

    def generate_custom(self, intervals, ratios, name="custom"):
        """
        A custom temperament can be defined with arbitrary rules.

        Parameters
        ----------
        intervals : list
            An ordered list of interval names to define per octave
            
        ratios : dict
            A dictionary of ratios to apply when generating the note
            frequencies in an octave. The dictionary keys are defined
            in the intervals list. Each ratio (between 1 and 2) is applied
            to the base frequency of the octave. The final frequency
            should always be equal to 2.

        name : str
            The name associated with the custom temperament
        """
        self.name = name

        self.octave_length = len(intervals)
        self.freqs = [self.base_frequency]

        for octave in range(self.number_of_octaves):
            c = self.freqs[-1]
            for i in range(self.octave_length):
                if i == 0:
                    continue
                self.freqs.append(c * ratios[intervals[i]])

        self.generate_generic_note_names()

    def __str__(self):
        """
        Returns
        -------
        str
            The list of frequencies
        """
        freqs = []
        for f in self.freqs:
            freqs.append("%0.2f" % (f + 0.005))
        return "%s temperament:\n\n%s" % (self.name, "\n".join(freqs))


class KeySignature:
    """
    A key signature is a set of sharp, flat, and natural symbols.
    """

    # Predefined modes are defined by the number of semitones between notes.
    MUSICAL_MODES = {
        # 12 notes in an octave
        "chromatic": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        # 8 notes in an octave
        "algerian": [2, 1, 2, 1, 1, 1, 3, 1],
        "diminished": [2, 1, 2, 1, 2, 1, 2, 1],
        "spanish": [1, 2, 1, 1, 1, 2, 2, 2],
        "octatonic": [1, 2, 1, 2, 1, 2, 1, 2],
        "bebop": [1, 1, 1, 2, 2, 1, 2, 2],
        # 7 notes in an octave
        "major": [2, 2, 1, 2, 2, 2, 1],
        "harmonic major": [2, 2, 1, 2, 1, 3, 1],
        "minor": [2, 1, 2, 2, 1, 2, 2],
        "natural minor": [2, 1, 2, 2, 1, 2, 2],
        "harmonic minor": [2, 1, 2, 2, 1, 3, 1],
        "melodic minor": [2, 1, 2, 2, 2, 2, 1],
        # "Church" modes
        "ionian": [2, 2, 1, 2, 2, 2, 1],
        "dorian": [2, 1, 2, 2, 2, 1, 2],
        "phrygian": [1, 2, 2, 2, 1, 2, 2],
        "lydian": [2, 2, 2, 1, 2, 2, 1],
        "mixolydian": [2, 2, 1, 2, 2, 1, 2],
        "aeolian": [2, 1, 2, 2, 1, 2, 2],
        "locrian": [1, 2, 2, 1, 2, 2, 2],
        "jazz minor": [2, 1, 2, 2, 2, 2, 1],
        "arabic": [2, 2, 1, 1, 2, 2, 2],
        "byzantine": [1, 3, 1, 2, 1, 3, 1],
        "enigmatic": [1, 3, 2, 2, 2, 1, 1],
        "ethiopian": [2, 1, 2, 2, 1, 2, 2],
        "geez": [2, 1, 2, 2, 1, 2, 2],
        "hindu": [2, 2, 1, 2, 1, 2, 2],
        "hungarian": [2, 1, 3, 1, 1, 3, 1],
        "maqam": [1, 3, 1, 2, 1, 3, 1],
        "romanian minor": [2, 1, 3, 1, 2, 1, 2],
        "spanish gypsy": [1, 3, 1, 2, 1, 2, 2],
        # 6 notes in an octave
        "minor blues": [3, 2, 1, 1, 3, 2],
        "major blues": [2, 1, 1, 3, 2, 2],
        "whole tone": [2, 2, 2, 2, 2, 2],
        # 5 notes in an octave
        "major pentatonic": [2, 2, 3, 2, 3],
        "minor pentatonic": [3, 2, 2, 3, 2],
        "chinese": [4, 2, 1, 4, 1],
        "egyptian": [2, 3, 2, 3, 2],
        "hirajoshi": [1, 4, 1, 4, 2],
        "in": [1, 4, 2, 1, 4],
        "minyo": [3, 2, 2, 3, 2],
        "fibonacci": [1, 1, 2, 3, 5],
    }

    # This notation only applies to temperaments with 12 semitones.
    PITCH_LETTERS = ["c", "d", "e", "f", "g", "a", "b"]
    SHARPS = ["c#", "d#", "f#", "g#", "a#"]
    FLATS = ["db", "eb", "gb", "ab", "bb"]

    # These note defintions are only relevant to equal temperament.
    NOTES_SHARP = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    NOTES_FLAT = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "bb", "b"]
    PREFER_SHARPS = [
        "g major",
        "d major",
        "a major",
        "e major",
        "b major",
        "e minor",
        "b minor",
        """
        "f# major",
        "e# major",
        "e# minor",
        "c# major",
        "d# major",
        "f# minor",
        "c# minor",
        "g# minor",
        "d# minor",
        """,
    ]
    PREFER_FLATS = [  # We default to preferring flats.
        "f major",
        "bb major",
        "eb major",
        "ab major",
        "db major",
        "gb major",
        "cb major",
        "d minor",
        "g minor",
        "c minor",
        "f minor",
        "bb minor",
        "eb minor",
        "d harmonic minor",
        "g harmonic minor",
        "c harmonic minor",
        "f harmonic minor",
        "bb harmonic minor",
        "eb harmonic minor",
    ]

    # The equivants and conversions are only valid for equal temperament.
    EQUIVALENT_FLATS = {"c#": "db", "d#": "eb", "f#": "gb", "g#": "ab", "a#": "bb"}
    EQUIVALENT_SHARPS = {"db": "c#", "eb": "d#", "gb": "f#", "ab": "g#", "bb": "a#"}
    EQUIVALENTS = {
        "ax": ["b", "cb"],
        "a#": ["bb"],
        "a": ["bbb", "gx"],
        "ab": ["g#"],
        "abb": ["g", "fx"],
        "bx": ["c#"],
        "b#": ["c", "dbb"],
        "b": ["b", "cb", "ax"],
        "bb": ["a#"],
        "bbb": ["a", "gx"],
        "cx": ["d"],
        "c#": ["db"],
        "c": ["c", "dbb", "b#"],
        "cb": ["b"],
        "cbb": ["bb", "a#"],
        "dx": ["e", "fb"],
        "d#": ["eb", "fbb"],
        "d": ["ebb", "cx"],
        "db": ["c#", "bx"],
        "dbb": ["c", "b#"],
        "ex": ["f#", "gb"],
        "e#": ["f", "gbb"],
        "e": ["e", "fb", "dx"],
        "eb": ["d#", "fbb"],
        "ebb": ["d", "cx"],
        "fx": ["g", "abb"],
        "f#": ["gb", "ex"],
        "f": ["f", "e#", "gbb"],
        "fb": ["e", "dx"],
        "fbb": ["eb", "d#"],
        "gx": ["a", "bbb"],
        "g#": ["ab"],
        "g": ["abb", "fx"],
        "gb": ["f#", "ex"],
        "gbb": ["f", "e#"],
    }
    CONVERT_DOWN = {
        "abb": "g",
        "ab": "g#",
        "a": "gx",
        "bb": "a#",
        "bbb": "a",
        "b": "ax",
        "c": "b#",
        "cb": "b",
        "c#": "bx",
        "d": "cx",
        "dbb": "c",
        "db": "c#",
        "e": "dx",
        "ebb": "d",
        "eb": "d#",
        "fb": "e",
        "f": "e#",
        "f#": "ex",
        "g": "fx",
        "gb": "f#",
        "gbb": "f",
    }
    CONVERT_UP = {
        "a#": "bb",
        "a": "bbb",
        "ab": "g#",
        "bb": "a#",
        "bbb": "a",
        "b#": "c",
        "b": "cb",
        "c#": "db",
        "c": "dbb",
        "db": "c#",
        "d#": "eb",
        "d": "ebb",
        "eb": "d#",
        "e#": "f",
        "e": "fb",
        "f#": "gb",
        "f": "gbb",
        "g#": "ab",
        "g": "abb",
        "gb": "f#",
    }

    def __init__(self, mode="major", key="c", number_of_semitones=12):
        """
        In defining a scale, we need to know the key, the mode, and the
        number of notes in the temperament used to define the scale.

        Parameters
        ----------
        mode : str
            One of the modes defined in self.MUSIC_MODES

        key : str
            Any pitch defined by in the temperament. (Note that currently
            the only notation supported is for temperaments with up to 12
            steps.

        number_of_semitones : int
            The number of semitones defined in the temperament

        NOTE: many of the class methods assume that the temperament has
        12 steps.
        """
        self.number_of_semitones = number_of_semitones

        # Define generic note names.
        self.note_names = []
        for i in range(self.number_of_semitones):
            self.note_names.append("n%d" % i)

        # We handle 12-semitone temperaments differently since they
        # can use letter name and predefined modes.
        if self.number_of_semitones == 12:
            if isinstance(mode, str):
                self.mode = mode.lower()
                if mode in self.MUSICAL_MODES:
                    self.mode = mode
                    self.half_steps = self.MUSICAL_MODES[self.mode]
            elif isinstance(mode, list):
                self.mode = "custom"
                # Check to see if the mode list is properly formed.
                if len(mode) > 12:
                    print("Too many half steps in mode definition.")
                    mode = self.MUSICAL_MODES["chromatic"]
                elif len(mode) < 1:
                    print("Too few half steps in mode definition.")
                    mode = self.MUSICAL_MODES["chromatic"]
                n = 0
                for i in range(len(mode)):
                    if not isinstance(mode[i], int):
                        print("NAN in mode definition.", mode[i])
                        mode[i] = 1
                    elif mode[i] < 1:
                        print("Mode increment must be > 0.", mode[i])
                        mode[i] = 1
                    n += mode[i]
                if n < 12:
                    mode[-1] += 12 - n
                if n > 12:
                    mode[-1] -= n - 12
                    if mode[-1] < 1:
                        mode = mode[:-1]
                self.half_steps = mode[:]
            else:
                print("Unknown mode %s. Defaulting to major mode" % (mode))
                self.mode = "major"
                self.half_steps = self.MUSICAL_MODES[self.mode]
            key = normalize_pitch(key)
            if key in self.NOTES_SHARP or key in self.NOTES_FLAT:
                self.key = key
            else:
                # Some special cases, including double sharps and flats.
                if key in ["cb", "fb", "e#", "b#"]:
                    self.key = key
                elif "x" in key and key in self.EQUIVALENTS:
                    self.key = self.EQUIVALENTS[key][0]
                elif "bb" in key and key in self.EQUIVALENTS:
                    self.key = self.EQUIVALENTS[key][0]
                elif "n" in key and key in self.note_names:
                    self.key = self.NOTES_SHARP[self.note_names.index(key)]
                else:
                    print("Unknown key %s. Defaulting to C" % (key))
                    self.key = "c"
        else:
            # Otherwise, we use the generic note names for everything.
            key = normalize_pitch(key)
            if key[0] != "n":
                self.key = "n0"
            else:
                # TO DO: Check key is valid
                self.key = key
            self.mode = "custom"
            if isinstance(mode, list):
                self.mode = "custom"
                # Check to see if the mode list is properly formed.
                if len(mode) > self.number_of_semitones:
                    print("Too many half steps in mode definition.")
                    mode = mode[: self.number_of_semitones]
                elif len(mode) < 1:
                    print("Too few half steps in mode definition.")
                    mode = [self.number_of_semitones]
                n = 0
                for i in range(len(mode)):
                    if not isinstance(mode[i], int):
                        print("NAN in mode definition.", mode[i])
                        mode[i] = 1
                    elif mode[i] < 1:
                        print("Mode increment must be > 0.", mode[i])
                        mode[i] = 1
                    n += mode[i]
                if n < self.number_of_semitones:
                    print("Mode definition is too low:", n)
                    mode[-1] += self.number_of_semitones - n
                if n > self.number_of_semitones:
                    print("Mode definition is too high:", n)
                    mode[-1] -= n - self.number_of_semitones
                    if mode[-1] < 1:
                        mode = mode[:-1]
                self.half_steps = mode[:]
            else:
                # Force mode to "chromatic"
                self.half_steps = []
                for i in range(self.number_of_semitones):
                    self.half_steps.append(1)

        self.key_signature = "%s %s" % (self.key, self.mode)
        self._build_scale()

    def get_scale(self):
        """
        The (scalar) notes in the scale.

        Returns
        -------
        list
            The (scalar) notes in the scale.

        NOTE: The internal definition of the scale includes the octave.
        """
        return self.scale[:-1]

    def get_mode_length(self):
        """
        How many notes are in the scale?

        Returns
        -------
        int
            The number of (scalar) notes in the scale.
        """
        return len(self.scale) - 1

    def get_number_of_semitones(self):
        """
        How many semitones (half-steps) are in the temperament used to
        define this key/mode?

        Returns
        -------
        int
            The number of semitones in the temperament used to define
            the scale
        """
        return self.number_of_semitones

    def set_note_names(self, note_names):
        """
        Generic note names are defined by the temperament.
        """
        self.note_names = note_names[:]

    def letter_name_to_note_name(self, pitch_name):
        """
        Convert from letter names used by 12-semitone temperaments to
        a generic note name as defined by the temperament.
        NOTE: Only for temperaments with 12 semitones.
        """
        pitch_name = normalize_pitch(pitch_name)
        # Maybe it is already a generic name.
        if pitch_name in self.note_names:
            return pitch_name, 0
        if self.number_of_semitones != 12:
            print("Cannot convert %s to a generic note name." % pitch_name)
            return "", -1

        if "#" in pitch_name and pitch_name in self.NOTES_SHARP:
            return self.note_names[self.NOTES_SHARP.index(pitch_name)], 0
        if pitch_name in self.NOTES_FLAT:
            return self.note_names[self.NOTES_FLAT.index(pitch_name)], 0

        print("Pitch name %s not found." % pitch_name)
        return "", -1

    def modal_pitch_to_letter(self, modal_index):
        """
        Given a modal number, return the corresponding pitch in the scale
        (and any change in octave).

        Parameters
        ----------
        modal_index : int
            The modal index specifies an index into the scale. If the
            index is >= mode length or < 0, a relative change in octave
            is also calculated.

        Returns
        -------
        str
            The pitch that is the result of indexing the scale by the
            modal index.

        int
            The relative change in octave due to mapping the modal index
            to the mode length
        """
        mode_length = self.get_mode_length()
        modal_index = int(modal_index)
        delta_octave = int(modal_index / mode_length)
        if modal_index < 0:
            delta_octave -= 1
            while modal_index < 0:
                modal_index += mode_length
        while modal_index > mode_length - 1:
            modal_index -= mode_length
        return self.scale[modal_index], delta_octave

    def note_in_scale(self, target):
        """
        Given a pitch, check to see if it is in the scale.

        Parameters
        ----------
        target : str
            The target pitch specified as a pitch letter, e.g., c#, fb.

        Returns
        -------
        boolean
            True if the note is in the scale
        """
        return self.closest_note(target)[2] == 0

    def semitone_transform(self, starting_pitch, number_of_half_steps):
        """
        Given a starting pitch, add a semitone transform and return
        the resultant pitch (and any change in octave).

        Parameters
        ----------
        starting_pitch : str
            The starting pitch specified as a pitch letter, e.g., c#, fb.

        number_of_half_steps : int
            Half steps are steps in the notes defined by the temperament

        Returns
        -------
        str
            The pitch that is the number of half steps from the starting
            pitch.

        int
            The relative change in octave between the starting pitch and the
            new pitch.

        int
            error code
        """
        starting_pitch = normalize_pitch(starting_pitch)
        mode_length = self.get_mode_length()
        delta_octave = 0
        if self.number_of_semitones == 12:
            if starting_pitch in self.NOTES_SHARP:
                i = self.NOTES_SHARP.index(starting_pitch)
                i += number_of_half_steps
                while i < 0:
                    i += self.number_of_semitones
                    delta_octave -= 1
                while i > self.number_of_semitones - 1:
                    i -= self.number_of_semitones
                    delta_octave += 1
                return self.NOTES_SHARP[i], delta_octave, 0
            elif starting_pitch in self.NOTES_FLAT:
                i = self.NOTES_FLAT.index(starting_pitch)
                i += number_of_half_steps
                while i < 0:
                    i += self.number_of_semitones
                    delta_octave -= 1
                while i > self.number_of_semitones - 1:
                    i -= self.number_of_semitones
                    delta_octave += 1
                return self.NOTES_FLAT[i], delta_octave, 0
            elif starting_pitch in self.note_names:
                i = self.note_names.index(starting_pitch)
                i += number_of_half_steps
                while i < 0:
                    i += self.number_of_semitones
                    delta_octave -= 1
                while i > self.number_of_semitones - 1:
                    i -= self.number_of_semitones
                    delta_octave += 1
                return self.note_names[i], delta_octave, 0
            else:
                print("Cannot find %s in note names." % starting_pitch)
                return starting_pitch, 0, -1
        else:
            if starting_pitch in self.note_names:
                i = self.note_names.index(starting_pitch)
                i += number_of_half_steps
                while i < 0:
                    i += self.number_of_semitones
                    delta_octave -= 1
                while i > self.number_of_semitones - 1:
                    i -= self.number_of_semitones
                    delta_octave += 1
                return self.note_names[i], delta_octave, 0
            else:
                print("Cannot find %s in note names." % starting_pitch)
                return starting_pitch, 0, -1

    def scalar_transform(self, starting_pitch, number_of_scalar_steps):
        """
        Given a starting pitch, add a scalar transform and return
        the resultant pitch (and any change in octave).

        Parameters
        ----------
        starting_pitch : str
            The starting pitch specified as a pitch letter, e.g., c#, fb.
            Note that the starting pitch may or may not be in the scale.

        number_of_scalar_steps : int
            Scalar steps are steps in the scale (as opposed to half-steps)

        Returns
        -------
        str
            The pitch that is the number of scalar steps from the starting
            pitch.

        int
            The relative change in octave between the starting pitch and the
            new pitch.

        int
            error code
        """

        starting_pitch = normalize_pitch(starting_pitch)

        # First, we need to find the closest note to our starting pitch.
        closest, closest_index, distance, error_code = self.closest_note(starting_pitch)
        if error_code < 0:
            return starting_pitch, 0, error_code

        # Next, we add the scalar interval -- the steps are in the
        # scale.
        new_index = closest_index + number_of_scalar_steps

        # We also need to determine if we will be travelling more than
        # one octave.
        mode_length = self.get_mode_length()
        delta_octave = int(new_index / mode_length)

        # We need an index value between 0 and mode length - 1.
        normalized_index = new_index
        while normalized_index < 0:
            normalized_index += mode_length
        while normalized_index > mode_length - 1:
            normalized_index -= mode_length
        new_note = self.scale[normalized_index]

        # We need to keep track of whether or not we crossed C, which
        # is the octave boundary.
        if new_index < 0:
            delta_octave -= 1

        # De we need to take into account the distance from the
        # closest scalar note?
        if distance == 0:
            return new_note, delta_octave

        # TODO: Handle accidentals for non-12-semitone temperaments
        if "#" in starting_pitch:
            i = self.NOTES_SHARP.index(new_note)
        else:
            i = self.NOTES_FLAT.index(new_note)
        i += distance
        if i < 0:
            i += mode_length
        elif i > mode_length:
            i -= mode_length

        if "#" in starting_pitch:
            return self.NOTES_SHARP[i], delta_octave
        return self.NOTES_FLAT[i], delta_octave

    def closest_note(self, target):
        """
        Given a target pitch, what is the closest note in the current
        key signature (key and mode)?

        Parameters
        ----------
        target : str
            target pitch specified as a pitch letter, e.g., c#, fb

        Returns
        -------
        str
            The closest pitch to the target pitch in the scale.
        int
            The scalar index value of the closest pitch in the scale
            (If the target is midway between two scalar pitches, the
            lower pitch is returned.)
        int
            The distance in semitones (half-steps) from the target
            pitch to the scalar pitch (If the target is higher than
            the scalar pitch, then distance > 0. If the target is
            lower than the scalar pitch then distance < 0. If the
            target matches a scale pitch, then distance = 0.)
        int
            error code (0 means success)
        """
        target = normalize_pitch(target)
        # Handle temperaments with more than 12 semitones separately.
        if self.number_of_semitones != 12:
            # First look for an exact match.
            for i in range(self.get_mode_length()):
                if target == self.scale[i]:
                    return target, i, 0, 0
            # Then look for the nearest note in the scale.
            if target in self.note_names:
                ti = self.note_names.index(target)
                # Look up for a note in the scale.
                distance = self.number_of_semitones
                n = 1
                for i in range(self.get_mode_length()):
                    if i < ti + 1:
                        continue
                    if self.note_names[i] in self.scale:
                        closest_note = self.note_names[i]
                        distance = n
                        break
                    n += 1
                # Look down.
                n = 1
                for i in range(ti):
                    if self.note_names[ti - i] in self.scale:
                        if n < distance:
                            return (
                                self.note_names[ti - i],
                                self.scale.index(self.note_names[ti - i]),
                                -n,
                                0,
                            )
                        n += 1
                if distance < self.number_of_semitones:
                    return closest_note, self.scale.index(closest_note), distance, 0

                print("Closest note to %s not found." % target)
                return target, 0, 0, -1

            print("Note %s not found." % target)
            return target, 0, 0, -1

        # First, try to find an exact match
        for i in range(self.get_mode_length()):
            if target == self.scale[i]:
                return target, i, 0, 0
        # Next, see if one of the equivalent notes matches
        for i in range(self.get_mode_length()):
            if target in self.EQUIVALENTS:
                for k in self.EQUIVALENTS[target]:
                    if k == self.scale[i]:
                        return self.scale[i], i, 0, 0
        # Finally, look for the closest note.
        closest = self.scale[0]
        closest_idx = 0
        closest_distance = self.number_of_semitones

        i2 = -1
        if target in self.NOTES_SHARP:
            i2 = self.NOTES_SHARP.index(target)
        elif target in self.NOTES_FLAT:
            i2 = self.NOTES_FLAT.index(target)
        else:
            for k in self.EQUIVALENTS[target]:
                if k in self.NOTES_SHARP:
                    i2 = self.NOTES_SHARP.index(k)
                    break
                elif k in self.NOTES_FLAT:
                    i2 = self.NOTES_FLAT.index(k)
                    break
        # This should never happen.
        if i2 == -1:
            print("Cannot find the position of target note %s" % (target))
            return closest, closest_idx, closest_distance, -1

        for i in range(self.get_mode_length()):
            this_note = self.scale[i]
            i1 = -1
            if this_note in self.NOTES_SHARP:
                i1 = self.NOTES_SHARP.index(this_note)
            elif this_note in self.NOTES_FLAT:
                i1 = self.NOTES_FLAT.index(this_note)
            else:
                for k in self.EQUIVALENTS[this_note]:
                    if k in self.NOTES_SHARP:
                        i1 = self.NOTES_SHARP.index(k)
                        break
                    elif k in self.NOTES_FLAT:
                        i1 = self.NOTES_FLAT.index(k)
                        break
            # This should never happen.
            if i1 == -1:
                print("Cannot find the position of %s" % (this_note))
                return closest, closest_idx, closest_distance, -1

            if abs(i2 - i1) < abs(closest_distance):
                closest = self.scale[i]
                closest_idx = i
                closest_distance = i2 - i1
            if abs(i2 + self.number_of_semitones - i1) < abs(closest_distance):
                closest = self.scale[i]
                closest_idx = i
                closest_distance = i2 + self.number_of_semitones - i1
        return closest, closest_idx, closest_distance, 0

    def _build_scale(self):
        """
        Given a key and mode, the scale is constructed. If the mode
        length is < 8, then it is enured that there are no duplicate
        letter names in the scale. Some key/mode combinations have a
        preference for sharps over flats. The default is to prefer
        flats over sharps.

        The constructed scale includes the octave value, hence it is
        one note longer than the mode.

        NOTE: This only works for temperaments with 12 semitones

        """
        key = self.key

        # If it is not a 12-semitone temperament, then we will use the
        # generic note names.
        if self.number_of_semitones != 12:
            this_scale = self.note_names
            # TODO: convert accidentals
            if key in this_scale:
                i = this_scale.index(key)
            else:
                i = 0
            self.scale = [self.key]
            for j in range(len(self.half_steps)):
                i += self.half_steps[j]
                self.scale.append(this_scale[i % self.number_of_semitones])
            self.scale[-1] = self.scale[0]
            return

        i = 0
        if self.key_signature in self.PREFER_SHARPS:
            this_scale = self.NOTES_SHARP
            if key in this_scale:
                i = this_scale.index(key)
            elif key in self.EQUIVALENT_SHARPS:
                i = this_scale.index(self.EQUIVALENT_SHARPS[key])
        else:
            this_scale = self.NOTES_FLAT
            if key in this_scale:
                i = this_scale.index(key)
            elif key in self.EQUIVALENT_FLATS:
                i = this_scale.index(self.EQUIVALENT_FLATS[key])

        # Special-case these virtual keys.
        if key == "e#":
            i = this_scale.index("f")
        elif key == "b#":
            i = this_scale.index("c")
        elif key == "cb":
            i = this_scale.index("b")
        elif key == "fb":
            i = this_scale.index("e")

        self.scale = [self.key]
        for j in range(len(self.half_steps)):
            i += self.half_steps[j]
            self.scale.append(this_scale[i % self.number_of_semitones])

        # At this point, the scale includes the first note of the next
        # octave. Hence, for example, the Latin modes hve 8 notes.
        if len(self.scale) < 9:
            # Convert to preferred accidental.
            if self.key_signature not in self.PREFER_SHARPS and "#" in self.key:
                for i in range(len(self.scale)):
                    if "b" in self.scale[i]:
                        if self.scale[i] in self.EQUIVALENT_SHARPS:
                            self.scale[i] = self.EQUIVALENT_SHARPS[self.scale[i]]

            # For Latin scales, we cannot skip notes.
            if len(self.scale) == 8:
                for i in range(len(self.scale) - 1):
                    i1 = self.PITCH_LETTERS.index(self.scale[i][0])
                    i2 = self.PITCH_LETTERS.index(self.scale[i + 1][0])
                    if i2 < i1:
                        i2 += 7
                    if i2 - i1 > 1:
                        if self.scale[i + 1] in self.CONVERT_DOWN:
                            self.scale[i + 1] = self.CONVERT_DOWN[self.scale[i + 1]]

            # And ensure there are no repeated letter names.
            for i in range(len(self.scale) - 1):
                if i == 0 and self.scale[i][0] == self.scale[i + 1][0]:
                    if self.scale[i + 1] in self.CONVERT_UP:
                        new_next_note = self.CONVERT_UP[self.scale[i + 1]]
                        self.scale[i + 1] = new_next_note
                elif self.scale[i][0] == self.scale[i + 1][0]:
                    if self.scale[i] in self.CONVERT_DOWN:
                        new_current_note = self.CONVERT_DOWN[self.scale[i]]
                    # If changing the current note makes it the same
                    # as the previous note, then we need to change the
                    # next note instead.
                    if new_current_note[0] != self.scale[i - 1][0]:
                        self.scale[i] = new_current_note
                    else:
                        if self.scale[i + 1] in self.CONVERT_UP:
                            new_next_note = self.CONVERT_UP[self.scale[i + 1]]
                            self.scale[i + 1] = new_next_note
        else:
            # Convert to preferred accidental.
            if "#" in self.key:
                for i in range(len(self.scale)):
                    if "b" in self.scale[i]:
                        if self.scale[i] in self.EQUIVALENT_SHARPS:
                            self.scale[i] = self.EQUIVALENT_SHARPS[self.scale[i]]
        # Make sure the notation for the last note in the scale (the
        # first note in the next octave) is in the same form as the
        # first note.
        self.scale[-1] = self.scale[0]

    def __str__(self):
        """
        Return the key, mode, number of half steps, and the scale.
        """
        half_steps = []
        for i in range(len(self.half_steps)):
            half_steps.append(str(self.half_steps[i]))
        hs = " ".join(half_steps)
        scale = " ".join(self.scale)
        if len(self.key) > 1:
            key = "%s%s" % (self.key[0].upper(), self.key[1:])
        else:
            key = self.key.upper()
        return "%s %s [%s] [%s]" % (key, self.mode.upper(), hs, scale)
