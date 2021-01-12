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

import re

from musicutils import strip_accidental, normalize_pitch


class Scale:
    """
    A scale is a selection of notes in an octave.
    """

    def __init__(self, half_steps_pattern=[], starting_index=0, number_of_semitones=12):
        """
        When defining a scale, we need the half steps pattern that defines
        the selection anf a starting note, e.g., C or F#,

        Parameters
        ----------
        half_steps_pattern : list
            A list of int values that define how many half steps to take
            between each note in the scale, e.g., [2, 2, 1, 2, 2, 2, 1]
            defines the steps for a Major scale

        starting_index : int
            An index into the half steps defining an octave that determines
            from where to start building the scale, e.g., 0 for C and 7 for G
            in a 12-step temperament

        number_of_semitones : int
            If the half_steps_pattern is an empty list, then the number of
            semitones instead
        """

        # Calculate the number of semitones by summing up the half
        # steps.
        if len(half_steps_pattern) == 0:
            self.number_of_semitones = number_of_semitones
            for i in range(self.number_of_semitones):
                half_steps_pattern.append(1)
        else:
            self.number_of_semitones = 0
            for i in range(len(half_steps_pattern)):
                self.number_of_semitones += half_steps_pattern[i]

        # Define generic note names that map to temperament.
        self.note_names = []
        for i in range(self.number_of_semitones):
            self.note_names.append("n%d" % i)

        i = starting_index % len(self.note_names)
        octave = 0
        self.scale = [self.note_names[i]]
        self.octave_deltas = [octave]
        for j in range(len(half_steps_pattern)):
            i += half_steps_pattern[j]
            if not i < self.number_of_semitones:
                octave += 1
                i -= self.number_of_semitones
            self.scale.append(self.note_names[i])
            self.octave_deltas.append(octave)

    def get_number_of_semitones(self):
        return len(self.note_names)

    def get_note_names(self):
        return self.note_names

    def get_scale(self, format=None):
        if format is None:
            return self.scale
        if len(format) == self.number_of_semitones:
            scale = []
            for i in range(len(self.scale)):
                scale.append(format[self.note_names.index(self.scale[i])])
            return scale
        print("format does not match number of semitones")
        return self.scale

    def get_scale_and_octave_deltas(self, format=None):
        return self.get_scale(format), self.octave_deltas


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

    # These maqam mode names imply a specific key.
    MAQAM_KEY_OVERRIDES = {
        "hijaz kar": "c",
        "hijaz kar maqam": "c",
        "shahnaz": "d",
        "maqam mustar": "eb",
        "maqam jiharkah": "f",
        "shadd araban": "g",
        "suzidil": "a",
        "ajam": "bb",
        "ajam maqam": "bb",
    }

    # Pitch name types
    GENERIC_NOTE_NAME = "generic note name"
    LETTER_NAME = "letter name"
    SOLFEGE_NAME = "solfege name"
    EAST_INDIAN_SOLFEGE_NAME = "east indian solfege name"
    SCALAR_MODE_NUMBER = "scalar mode number"
    CUSTOM_NAME = "custom name"
    UNKNOWN = "unknown"

    # This notation only applies to temperaments with 12 semitones.
    PITCH_LETTERS = ["c", "d", "e", "f", "g", "a", "b"]
    SCALAR_MODE_NUMBERS = ["1", "2", "3", "4", "5", "6", "7"]
    SOLFEGE_NAMES = ["do", "re", "me", "fa", "sol", "la", "ti"]
    EAST_INDIAN_NAMES = ["sa", "re", "ga", "ma", "pa", "dha", "ni"]

    # These defintions are only relevant to equal temperament.
    NOTES_SHARP = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    NOTES_FLAT = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "bb", "b"]
    SOLFEGE_SHARP = [
        "do",
        "do#",
        "re",
        "re#",
        "me",
        "fa",
        "fa#",
        "sol",
        "sol#",
        "la",
        "la#",
        "ti",
    ]
    SOLFEGE_FLAT = [
        "do",
        "reb",
        "re",
        "meb",
        "me",
        "fa",
        "solb",
        "sol",
        "lab",
        "la",
        "tib",
        "ti",
    ]
    EAST_INDIAN_SHARP = [
        "sa",
        "sa#",
        "re",
        "re#",
        "ga",
        "ma",
        "ma#",
        "pa",
        "pa#",
        "dha",
        "dha#",
        "ni",
    ]
    EAST_INDIAN_FLAT = [
        "sa",
        "reb",
        "re",
        "gab",
        "ga",
        "ma",
        "pab",
        "pa",
        "dhab",
        "dha",
        "nib",
        "ni",
    ]
    SCALAR_NAMES_SHARP = [
        "1",
        "1#",
        "2",
        "2#",
        "3",
        "4",
        "4#",
        "5",
        "5#",
        "6",
        "6#",
        "7",
    ]
    SCALAR_NAMES_FLAT = [
        "1",
        "2b",
        "2",
        "3b",
        "3",
        "4",
        "4b",
        "5",
        "6b",
        "6",
        "7b",
        "7",
    ]

    MODE_MAPPER = {
        "ionian": "major",
        "aeolian": "minor",
        "natural minor": "minor",
        "harmonic minor": "minor",
        "major": "major",
        "minor": "minor",
    }

    # These key signaturs (and their equivalents) prefer sharps over flats.
    PREFER_SHARPS = [
        "c major",
        "c major pentatonic",
        "c major blues",
        "c whole tone",
        "d dorian",
        "e phrygian",
        "f lydian",
        "g mixolydian",
        "a minor",
        "a minor pentatonic",
        "b locrian",
        "g major",
        "g major pentatonic",
        "g major blues",
        "g whole tone",
        "a dorian",
        "b phrygian",
        "c lydian",
        "d mixolydian",
        "e minor",
        "e minor pentatonic",
        "f# locrian",
        "d major",
        "d major pentatonic",
        "d major blues",
        "d whole tone",
        "e dorian",
        "f# phrygian",
        "g lydian",
        "a mixolydian",
        "b minor",
        "b minor pentatonic",
        "c# locrian",
        "a major",
        "a major pentatonic",
        "a major blues",
        "a whole tone",
        "b dorian",
        "c# phrygian",
        "d lydian",
        "e mixolydian",
        "f# minor",
        "f# minor pentatonic",
        "e major",
        "e major pentatonic",
        "e major blues",
        "e whole tone",
        "f# dorian",
        "a lydian",
        "b mixolydian",
        "c# minor",
        "c# minor pentatonic",
        "b major",
        "b major pentatonic",
        "b major blues",
        "b whole tone",
        "c# dorian",
        "d# phrygian",
        "e lydian",
        "f# mixolydian",
        "g# minor",
        "g# minor pentatonic",
        "a# locrian",
    ]

    # The equivants and conversions are only valid for equal temperament.
    EQUIVALENT_FLATS = {
        "c#": "db",
        "d#": "eb",
        "f#": "gb",
        "g#": "ab",
        "a#": "bb",
        "e#": "f",
        "b#": "c",
        "cb": "cb",
        "fb": "fb",
    }
    EQUIVALENT_SHARPS = {
        "db": "c#",
        "eb": "d#",
        "gb": "f#",
        "ab": "g#",
        "bb": "a#",
        "cb": "b",
        "fb": "e",
        "e#": "e#",
        "b#": "b#",
    }
    EQUIVALENTS = {
        "ax": ["b", "cb"],
        "a#": ["bb"],
        "a": ["a", "bbb", "gx"],
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
        "d": ["d", "ebb", "cx"],
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
        "g": ["g", "abb", "fx"],
        "gb": ["f#", "ex"],
        "gbb": ["f", "e#"],
    }
    CONVERT_DOWN = {
        "c": "b#",
        "cb": "b",
        "cbb": "a#",
        "d": "cx",
        "db": "c#",
        "dbb": "c",
        "e": "dx",
        "eb": "d#",
        "ebb": "d",
        "f": "e#",
        "fb": "e",
        "fbb": "d#",
        "g": "fx",
        "gb": "f#",
        "gbb": "f",
        "a": "gx",
        "ab": "g#",
        "abb": "g",
        "b": "ax",
        "bb": "a#",
        "bbb": "a",
    }
    CONVERT_UP = {
        "cx": "d",
        "c#": "db",
        "c": "dbb",
        "dx": "e",
        "d#": "eb",
        "d": "ebb",
        "ex": "f#",
        "e#": "f",
        "e": "fb",
        "fx": "g",
        "f#": "gb",
        "f": "gbb",
        "gx": "a",
        "g#": "ab",
        "g": "abb",
        "ax": "b",
        "a#": "bb",
        "a": "bbb",
        "bx": "c#",
        "b#": "c",
        "b": "cb",
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
        """

        if isinstance(mode, str):
            mode = mode.lower()
            # Some mode names imply a specific key.
            if mode in self.MAQAM_KEY_OVERRIDES:
                # Override the key.
                key = self.MAQAM_KEY_OVERRIDES[mode]
                mode = "maqam"
            if mode in self.MUSICAL_MODES:
                self.mode = mode
                self.half_steps = self.MUSICAL_MODES[self.mode]
            else:
                print("mode not found")
                self.mode = "chromatic"
                self.half_steps = self.MUSICAL_MODES[self.mode]
        elif isinstance(mode, list):
            self.mode = "custom"  # We could look for a match
            self.half_steps = mode
        self.key = key
        i = 0
        if isinstance(self.key, str):
            key = normalize_pitch(key)
            if self._prefer_sharps(self.key, self.mode) or "#" in self.key:
                if not self.key in self.NOTES_SHARP:
                    self.key = self.EQUIVALENT_SHARPS[self.key]
                i = self.find_sharp_index(self.key)
            elif self.key in self.NOTES_FLAT or "b" in self.key:
                if not self.key in self.NOTES_FLAT:
                    self.key = self.EQUIVALENT_FLATS[self.key]
                i = self.find_flat_index(self.key)
            elif self.key[0] == "n" and self.key[1:].isdecimal():
                i = int(self.key[1:])  # This is not very robust.
            else:
                print("Could not find key index:", self.key)
        elif isinstance(self.key, int):
            i = self.key
        else:
            print("bad key type", type(key))

        if len(self.half_steps) == 0:
            self._scale = Scale(
                starting_index=i, number_of_semitones=self.number_of_semitones
            )
        else:
            self._scale = Scale(half_steps_pattern=self.half_steps, starting_index=i)

        self.generic_scale = self._scale.get_scale()
        self.number_of_semitones = self._scale.get_number_of_semitones()
        self.fixed_solfege = False

        if self.number_of_semitones == 12:
            if isinstance(self.key, int):
                self.key = self.NOTES_SHARP[self.key]
            self.note_names = self._scale.get_note_names()
            if self._prefer_sharps(self.key, self.mode) or "#" in self.key:
                scale = self._scale.get_scale(format=self.NOTES_SHARP)
            else:
                scale = self._scale.get_scale(format=self.NOTES_FLAT)
            # In generating the scale, the key may have been
            # switched to an equivalent.
            scale[0] = self.key
            scale[-1] = self.key
            self.scale = self.normalize_scale(scale)
            self._assign_solfege_note_names()
            self._assign_east_indian_solfege_note_names()
            self._assign_scalar_mode_numbers()
        else:
            self.note_names = self._scale.get_note_names()
            self.scale = self._scale.get_scale()
            if isinstance(self.key, int):
                self.key = self.note_names
            self.solfege_notes = []
            self.east_indian_solfege_notes = []
            self.scalar_mode_numbers = []

        self.custom_note_names = []

        self.key_signature = "%s %s" % (self.key, self.mode)

    def set_fixed_solfege(self, state=False):
        self.fixed_solfege = state

    def get_fixed_solfege(self):
        return self.fixed_solfege

    def is_a_sharp(self, pitch_name):
        if pitch_name.endswith("#") or pitch_name in self.PITCH_LETTERS:
            return True
        return False

    def find_sharp_index(self, pitch_name):
        if pitch_name in self.NOTES_SHARP:
            return self.NOTES_SHARP.index(pitch_name)
        if pitch_name in self.CONVERT_UP:
            new_pitch_name = self.CONVERT_UP[pitch_name]
            if new_pitch_name in self.NOTES_SHARP:
                return self.NOTES_SHARP.index(new_pitch_name)
        print("Could not find sharp index for", pitch_name)
        return 0

    def is_a_flat(self, pitch_name):
        if pitch_name.endswith("b") or pitch_name in self.PITCH_LETTERS:
            return True
        return False

    def find_flat_index(self, pitch_name):
        if pitch_name in self.NOTES_FLAT:
            return self.NOTES_FLAT.index(pitch_name)
        if pitch_name in self.CONVERT_DOWN:
            new_pitch_name = self.CONVERT_DOWN[pitch_name]
            if new_pitch_name in self.NOTES_FLAT:
                return self.NOTES_FLAT.index(new_pitch_name)
        print("Could not find flat index for", pitch_name)
        return 0

    def normalize_scale(self, scale):
        # At this point, the scale includes the first note of the next
        # octave. Hence, for example, the Latin modes hve 8 notes.
        if len(scale) < 9:
            # Convert to preferred accidental.
            if not self._prefer_sharps(self.key, self.mode) and "#" in self.key:
                for i in range(len(scale)):
                    if "b" in scale[i]:
                        if scale[i] in self.EQUIVALENT_SHARPS:
                            scale[i] = self.EQUIVALENT_SHARPS[scale[i]]

            # For Latin scales, we cannot skip notes.
            if len(scale) == 8:
                for i in range(len(scale) - 1):
                    i1 = self.PITCH_LETTERS.index(scale[i][0])
                    i2 = self.PITCH_LETTERS.index(scale[i + 1][0])
                    if i2 < i1:
                        i2 += 7
                    if i2 - i1 > 1:
                        if scale[i + 1] in self.CONVERT_DOWN:
                            scale[i + 1] = self.CONVERT_DOWN[scale[i + 1]]
            # And ensure there are no repeated letter names.
            for i in range(len(scale) - 1):
                if i == 0 and scale[i][0] == scale[i + 1][0]:
                    if scale[i + 1] in self.CONVERT_UP:
                        new_next_note = self.CONVERT_UP[scale[i + 1]]
                        scale[i + 1] = new_next_note
                elif scale[i][0] == scale[i + 1][0]:
                    if scale[i] in self.CONVERT_DOWN:
                        new_current_note = self.CONVERT_DOWN[scale[i]]
                    else:
                        print(scale[i])
                    # If changing the current note makes it the same
                    # as the previous note, then we need to change the
                    # next note instead.
                    if new_current_note[0] != scale[i - 1][0]:
                        scale[i] = new_current_note
                    else:
                        if scale[i + 1] in self.CONVERT_UP:
                            new_next_note = self.CONVERT_UP[scale[i + 1]]
                            scale[i + 1] = new_next_note
        else:
            # Convert to preferred accidental.
            if "#" in self.key:
                for i in range(len(scale)):
                    if "b" in scale[i]:
                        if scale[i] in self.EQUIVALENT_SHARPS:
                            scale[i] = self.EQUIVALENT_SHARPS[scale[i]]

        convert_up = False
        convert_down = False
        for i in range(len(scale)):
            if "x" in scale[i]:
                convert_up = True
                break
            if len(scale[i]) > 2:
                convert_down = True
        if convert_up:
            for i in range(len(scale)):
                if "x" in scale[i]:
                    scale[i] = self.CONVERT_UP[scale[i]]
                if scale[i] in self.EQUIVALENT_FLATS:
                    scale[i] = self.EQUIVALENT_FLATS[scale[i]]
        elif convert_down:
            for i in range(len(scale)):
                if len(scale[i]) > 2:
                    scale[i] = self.CONVERT_DOWN[scale[i]]
                if scale[i] in self.EQUIVALENT_SHARPS:
                    scale[i] = self.EQUIVALENT_SHARPS[scale[i]]
        return scale

    def _mode_map_list(self, source_list):
        """
        Given a list of names, map them to the current mode.

        Parameters
        ----------
        source_list : list
            List of names, e.g., Solfege names

        Returns
        -------
        list
            List of names mapped to the mode
        """
        return_list = []
        mode_length = self.get_mode_length()
        offset = "cdefgab".index(self.scale[0][0])
        for i in range(len(self.scale)):
            j = "cdefgab".index(self.scale[i][0]) - offset
            if j < 0:
                j += len(source_list)
            if mode_length < 8:
                # We ensured a unique letter name for each note when we
                # built the scale.
                return_list.append(source_list[j])
            else:
                # Some letters are repeated, so we need the accidentals.
                a = strip_accidental(self.scale[i])[1]
                if a == 0:
                    return_list.append(source_list[j])
                elif a == 1:
                    return_list.append(source_list[j] + "#")
                elif a == -1:
                    return_list.append(source_list[j] + "b")
                elif a == 2:
                    return_list.append(source_list[j] + "x")
                elif a == -2:
                    return_list.append(source_list[j] + "bb")
        return_list[-1] = return_list[0]
        return return_list

    def _assign_solfege_note_names(self):
        """
        Create a Solfege mapping of the scale ("fixed Solfege == True")

        Examples:
        Major: ['do', 're', 'me', 'fa', 'sol', 'la', 'ti', 'do']
        Major Pentatonic: ['do', 're', 'me', 'sol', 'la', 'do']
        Minor Pentatonic: ['do', 'me', 'fa', 'sol', 'ti', 'do']
        Whole Tone: ['do', 're', 'me', 'sol', 'la', 'ti', 'do']
        NOTE: Solfege assignment only works for temperaments of 12 semitones.
        """
        self.solfege_notes = []

        if self.number_of_semitones != 12:
            # TODO: We should make an exception for temperaments of 24
            # quartertones.
            print("No solfege for temperaments with more than 12 semitones.")
            return

        self.solfege_notes = self._mode_map_list(self.SOLFEGE_NAMES)

    def _assign_east_indian_solfege_note_names(self):
        """
        East Indian Solfege
        NOTE: Solfege assignment only works for temperaments of 12 semitones.
        """
        self.east_indian_solfege_notes = []

        if self.number_of_semitones != 12:
            # TODO: We should make an exception for temperaments of 24
            # quartertones.
            print("No solfege for temperaments with more than 12 semitones.")
            return

        self.east_indian_solfege_notes = self._mode_map_list(self.EAST_INDIAN_NAMES)

    def _assign_scalar_mode_numbers(self):
        """
        Scalar mode numbers refer to the available notes in the mode
        NOTE: Assignment only works for temperaments of 12 semitones.
        """
        self.scalar_mode_numbers = []

        if self.number_of_semitones != 12:
            # TODO: We should make an exception for temperaments of 24
            # quartertones.
            print("No mode numbers for temperaments with more than 12 semitones.")
            return

        self.scalar_mode_numbers = self._mode_map_list(self.SCALAR_MODE_NUMBERS)

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

    def set_custom_note_names(self, custom_names):
        """
        Custom note names defined by user

        Parameters
        ----------
        custom_names : list
            A list of custom names

        Note: Names should not end with b or x or they will cause
        collisions with the flat (b) and doublesharp (x) accidentals.
        """
        if len(custom_names) != self.get_mode_length():
            print("A unique name must be assigned to every note in the mode.")
            return -1
        self.custom_note_names = custom_names[:]
        return 0

    def get_custom_note_names(self):
        """
        Custom note names defined by user

        Returns
        -------
        list
            Custom names
        """
        return self.custom_note_names

    def _name_converter(self, pitch_name, source_list):
        """
        Convert from a source name, e.g., Solfege, to a note name.
        """
        if pitch_name in source_list:
            i = source_list.index(pitch_name)
            return self.convert_to_generic_note_name(self.scale[i])[0]
        pitch_name, delta = strip_accidental(pitch_name)
        if pitch_name in source_list:
            i = source_list.index(pitch_name)
            note_name = self.convert_to_generic_note_name(self.scale[i])[0]
            i = self.note_names.index(note_name)
            i += delta
            if i < 0:
                i += self.number_of_semitones
            if i > self.number_of_semitones - 1:
                i -= self.number_of_semitones
            return self.note_names[i]
        return None

    def convert_to_generic_note_name(self, pitch_name):
        """
        Convert from a letter name used by 12-semitone temperaments to
        a generic note name as defined by the temperament.
        NOTE: Only for temperaments with 12 semitones.
        """
        pitch_name = normalize_pitch(pitch_name)
        original_notation = self.get_pitch_type(pitch_name)

        # Maybe it is already a generic name.
        if original_notation == self.GENERIC_NOTE_NAME:
            return pitch_name, 0

        if original_notation == self.LETTER_NAME:
            # Look for a letter name, e.g., g# or ab
            if "#" in pitch_name and self.is_a_sharp(pitch_name):
                return self.note_names[self.find_sharp_index(pitch_name)], 0
            if self.is_a_flat(pitch_name):
                return self.note_names[self.find_flat_index(pitch_name)], 0
            # Catch cb, bx, etc.
            if pitch_name in self.EQUIVALENT_SHARPS:
                return (
                    self.note_names[
                        self.NOTES_SHARP.index(self.EQUIVALENT_SHARPS[pitch_name])
                    ],
                    0,
                )
            if pitch_name in self.EQUIVALENT_FLATS:
                return (
                    self.note_names[
                        self.find_flat_index(self.EQUIVALENT_FLATS[pitch_name])
                    ],
                    0,
                )
            if pitch_name in self.EQUIVALENTS:
                if "#" in self.EQUIVALENTS[pitch_name][0]:
                    return (
                        self.note_names[
                            self.find_sharp_index(self.EQUIVALENTS[pitch_name][0])
                        ],
                        0,
                    )
                return (
                    self.note_names[
                        self.find_flat_index(self.EQUIVALENTS[pitch_name][0])
                    ],
                    0,
                )

        if original_notation == self.SOLFEGE_NAME:
            # Look for a Solfege name
            if self.fixed_solfege:
                note_name = self._name_converter(pitch_name, self.solfege_notes)
                if note_name is not None:
                    return note_name, 0
            else:
                if "#" in pitch_name and pitch_name in self.SOLFEGE_SHARP:
                    return self.note_names[self.SOLFEGE_SHARP.index(pitch_name)], 0
                if pitch_name in self.SOLFEGE_FLAT:
                    return self.note_names[self.SOLFEGE_FLAT.index(pitch_name)], 0

        if original_notation == self.CUSTOM_NAME:
            # Look for a Custom name
            if len(self.custom_note_names) > 0:
                note_name = self._name_converter(pitch_name, self.custom_note_names)
                if note_name is not None:
                    return note_name, 0
            # Look for a Scalar mode number
            if self.fixed_solfege:
                note_name = self._name_converter(pitch_name, self.scalar_mode_numbers)
                if note_name is not None:
                    return note_name, 0
            else:
                if "#" in pitch_name and pitch_name in self.SCALAR_NAMES_SHARP:
                    return self.note_names[self.SCALAR_NAMES_SHARP.index(pitch_name)], 0
                if pitch_name in self.SCALAR_NAMES_FLAT:
                    return self.note_names[self.SCALAR_NAMES_FLAT.index(pitch_name)], 0

        if original_notation == self.EAST_INDIAN_SOLFEGE_NAME:
            # Look for a East Indian Solfege name
            if self.fixed_solfege:
                note_name = self._name_converter(
                    pitch_name, self.east_indian_solfege_notes
                )
                if note_name is not None:
                    return note_name, 0
            else:
                if "#" in pitch_name and pitch_name in self.EAST_INDIAN_SHARP:
                    return self.note_names[self.EAST_INDIAN_SHARP.index(pitch_name)], 0
                if pitch_name in self.EAST_INDIAN_FLAT:
                    return self.note_names[self.EAST_INDIAN_FLAT.index(pitch_name)], 0

        if original_notation == self.SCALAR_MODE_NUMBER:
            # Look for a scalar mode number
            if self.fixed_solfege:
                note_name = self._name_converter(pitch_name, self.scalar_mode_numbers)
                if note_name is not None:
                    return note_name, 0
            else:
                if "#" in pitch_name and pitch_name in self.SCALAR_NAMES_SHARP:
                    return self.note_names[self.SCALAR_NAMES_SHARP.index(pitch_name)], 0
                if pitch_name in self.SCALAR_NAMES_FLAT:
                    return self.note_names[self.SCALAR_NAMES_FLAT.index(pitch_name)], 0

        print("Pitch name %s not found." % pitch_name)
        return pitch_name, -1

    def generic_note_name_to_letter_name(self, note_name, prefer_sharps=True):
        """
        Convert from a generic note name as defined by the temperament
        to a letter name used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """
        note_name = normalize_pitch(note_name)
        # Maybe it is already a letter name?
        if self.is_a_sharp(note_name):
            return note_name, 0
        if self.is_a_flat(note_name):
            return note_name, 0
        if self.number_of_semitones != 12:
            print("Cannot convert %s to a letter name." % note_name)
            return note_name, -1

        if note_name in self.note_names:
            if prefer_sharps:
                return self.NOTES_SHARP[self.note_names.index(note_name)], 0
            return self.NOTES_FLAT[self.note_names.index(note_name)], 0

        print("Note name %s not found." % note_name)
        return note_name, -1

    def _convert_from_note_name(self, note_name, target_list):
        note_name = normalize_pitch(note_name)
        # Maybe it is already in the list?
        if note_name in target_list:
            return note_name, 0
        if self.number_of_semitones != 12:
            print("Cannot convert %s to a letter name." % note_name)
            return note_name, -1

        if note_name in self.note_names:
            # First find the corresponding letter name
            letter_name = self.NOTES_SHARP[self.note_names.index(note_name)]
            # Next, find the closest note in the scale.
            closest, i, distance, e = self.closest_note(letter_name)
            # Use the index to get the corresponding solfege note
            if distance == 0:
                return target_list[i], 0
            # Remove any accidental
            target_note, delta = strip_accidental(target_list[i])
            # Add back in the appropriate accidental
            delta += distance
            if delta == 0:
                return target_note, 0
            elif delta == -1:
                return target_note + "b", 0
            elif delta == 1:
                return target_note + "#", 0
            elif delta == -2:
                return target_note + "bb", 0
            elif delta == 2:
                return target_note + "#", 0
            else:
                print(
                    "Could not add accidental for delta %d to %s."
                    % (delta, target_note)
                )
                return target_note, -1

        print("Note name %s not found." % note_name)
        return note_name, -1

    def _find_moveable(self, note_name, sharp_scale, flat_scale, prefer_sharps):
        note_name = normalize_pitch(note_name)
        # Maybe it is already solfege?
        if note_name in sharp_scale:
            return note_name, 0
        if note_name in flat_scale:
            return note_name, 0
        if self.number_of_semitones != 12:
            print("Cannot convert %s to a letter name." % note_name)
            return note_name, -1

        if note_name in self.note_names:
            if prefer_sharps:
                return sharp_scale[self.note_names.index(note_name)], 0
            return flat_scale[self.note_names.index(note_name)], 0

    def generic_note_name_to_solfege(self, note_name, prefer_sharps=True):
        """
        Convert from a generic note name as defined by the temperament
        to a solfege note used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """
        if self.fixed_solfege:
            return self._convert_from_note_name(note_name, self.solfege_notes)

        return self._find_moveable(
            note_name, self.SOLFEGE_SHARP, self.SOLFEGE_FLAT, prefer_sharps
        )

    def generic_note_name_to_east_indian_solfege(self, note_name, prefer_sharps=True):
        """
        Convert from a generic note name as defined by the temperament
        to an East Indian solfege note used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        if self.fixed_solfege:
            return self._convert_from_note_name(
                note_name, self.east_indian_solfege_notes
            )

        return self._find_moveable(
            note_name, self.EAST_INDIAN_SHARP, self.EAST_INDIAN_FLAT, prefer_sharps
        )

    def generic_note_name_to_scalar_mode_number(self, note_name, prefer_sharps=True):
        """
        Convert from a generic note name as defined by the temperament
        to a scalar mode number used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        if self.fixed_solfege:
            return self._convert_from_note_name(note_name, self.scalar_mode_numbers)

        return self._find_moveable(
            note_name, self.SCALAR_NAMES_SHARP, self.SCALAR_NAMES_FLAT, prefer_sharps
        )

    def generic_note_name_to_custom_note_name(self, note_name):
        """
        Convert from a generic note name as defined by the temperament
        to a custom_note_name used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        return self._convert_from_note_name(note_name, self.custom_note_names)

    def get_pitch_type(self, pitch_name):
        """
        Pitches can be specified as a letter name, a solfege name, etc.
        """
        pitch_name = normalize_pitch(pitch_name)
        if pitch_name in self.NOTES_SHARP:
            return self.LETTER_NAME
        if pitch_name in self.NOTES_FLAT:
            return self.LETTER_NAME
        if pitch_name in self.EQUIVALENT_SHARPS:
            return self.LETTER_NAME
        if pitch_name in self.EQUIVALENT_FLATS:
            return self.LETTER_NAME
        pitch_name = strip_accidental(pitch_name)[0]
        if pitch_name[0] == "n" and pitch_name[1:].isdecimal():
            return self.GENERIC_NOTE_NAME
        if pitch_name in self.SOLFEGE_NAMES:
            return self.SOLFEGE_NAME
        if pitch_name in self.EAST_INDIAN_NAMES:
            return self.EAST_INDIAN_SOLFEGE_NAME
        if pitch_name in self.SCALAR_MODE_NUMBERS:
            return self.SCALAR_MODE_NUMBER
        if pitch_name in self.custom_note_names:
            return self.CUSTOM_NAME
        return self.UNKNOWN

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

    def _map_to_semitone_range(self, i, delta_octave):
        """
        Ensure that an index value is within the range of the temperament, e.g.,
        i == 12 would be mapped to 0 with a change in octave +1 for a
        temperament with 12 semitones.

        Parameters
        ----------
        i : int
            Index value into semitones

        delta_octave : int
            Any previous change in octave that needs to be preserved

        Returns
        -------
        int
            Index mapped to semitones

        int
            Any additonal change in octave due to mapping
        """
        while i < 0:
            i += self.number_of_semitones
            delta_octave -= 1
        while i > self.number_of_semitones - 1:
            i -= self.number_of_semitones
            delta_octave += 1
        return i, delta_octave

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
        original_notation = self.get_pitch_type(starting_pitch)
        mode_length = self.get_mode_length()
        delta_octave = 0
        if self.number_of_semitones == 12:
            if original_notation == self.LETTER_NAME:
                if self.is_a_sharp(starting_pitch):
                    i = self.find_sharp_index(starting_pitch)
                    i += number_of_half_steps
                    i, delta_octave = self._map_to_semitone_range(i, delta_octave)
                    return self.NOTES_SHARP[i], delta_octave, 0
                if self.is_a_flat(starting_pitch):
                    i = self.find_flat_index(starting_pitch)
                    i += number_of_half_steps
                    i, delta_octave = self._map_to_semitone_range(i, delta_octave)
                    return self.NOTES_FLAT[i], delta_octave, 0
                stripped_pitch, delta = strip_accidental(starting_pitch)
                if stripped_pitch in self.note_names:
                    note_name = stripped_pitch
                    e = 0
                else:
                    note_name, e = self.convert_to_generic_note_name(stripped_pitch)
                if e == 0:
                    if note_name in self.note_names:
                        i = self.note_names.index(note_name)
                        i += number_of_half_steps
                        i, delta_octave = self._map_to_semitone_range(
                            i + delta, delta_octave
                        )
                        return self.note_names[i], delta_octave, 0
                print("Cannot find %s in note names." % starting_pitch)
                return starting_pitch, 0, -1

            note_name, e = self.convert_to_generic_note_name(starting_pitch)
            stripped_pitch, delta = strip_accidental(note_name)  # starting_pitch)
            if stripped_pitch in self.note_names:
                i = self.note_names.index(stripped_pitch)
                i += number_of_half_steps
                i, delta_octave = self._map_to_semitone_range(i + delta, delta_octave)
                if original_notation == self.SOLFEGE_NAME:
                    return (
                        self.generic_note_name_to_solfege(
                            self.note_names[i], "#" in starting_pitch
                        )[0],
                        delta_octave,
                        0,
                    )
                if original_notation == self.EAST_INDIAN_SOLFEGE_NAME:
                    return (
                        self.generic_note_name_to_east_indian_solfege(
                            self.note_names[i], "#" in starting_pitch
                        )[0],
                        delta_octave,
                        0,
                    )
                if original_notation == self.SCALAR_MODE_NUMBER:
                    return (
                        self.generic_note_name_to_scalar_mode_number(
                            self.note_names[i], "#" in starting_pitch
                        )[0],
                        delta_octave,
                        0,
                    )
                return self.note_names[i], delta_octave, 0
            print("Cannot find %s in note names." % starting_pitch)
            return starting_pitch, 0, -1
        else:
            stripped_pitch, delta = strip_accidental(starting_pitch)
            if stripped_pitch in self.note_names:
                i = self.note_names.index(stripped_pitch)
                i += number_of_half_steps
                i, delta_octave = self._map_to_semitone_range(i + delta, delta_octave)
                return self.note_names[i], delta_octave, 0
            print("Cannot find %s in note names." % starting_pitch)
            return starting_pitch, 0, -1

    def _map_to_scalar_range(self, i, delta_octave):
        """
        Ensure that an index value is within the range of the scale, e.g.,
        i == 8 would be mapped to 0 with a change in octave +1 for a
        7-tone scale.

        Parameters
        ----------
        i : int
            Index value into scale

        delta_octave : int
            Any previous change in octave that needs to be preserved

        Returns
        -------
        int
            Index mapped to scale

        int
            Any additonal change in octave due to mapping
        """
        mode_length = self.get_mode_length()
        while i < 0:
            i += mode_length
            delta_octave -= 1
        while i > mode_length - 1:
            i -= mode_length
            delta_octave += 1
        return i, delta_octave

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
        original_notation = self.get_pitch_type(starting_pitch)
        prefer_sharps = "#" in starting_pitch
        # The calculation is done in the generic note namespace
        generic_pitch = self.convert_to_generic_note_name(starting_pitch)[0]

        # First, we need to find the closest note to our starting
        # pitch.
        closest, closest_index, distance, e = self.closest_note(generic_pitch)
        if e < 0:
            return starting_pitch, 0, e

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
        generic_new_note = self.generic_scale[normalized_index]
        new_note = self._restore_format(
            generic_new_note, original_notation, prefer_sharps
        )

        # We need to keep track of whether or not we crossed C, which
        # is the octave boundary.
        if new_index < 0:
            delta_octave -= 1

        # Do we need to take into account the distance from the
        # closest scalar note?
        if distance == 0:
            return new_note, delta_octave
        i = self.note_names.index(generic_new_note)
        i, delta_octave = self._map_to_scalar_range(i + distance, delta_octave)
        return (
            self._restore_format(self.note_names[i], original_notation, prefer_sharps),
            delta_octave,
        )

    def _restore_format(self, pitch_name, original_notation, prefer_sharps):
        """
        Format convertor (could be done with a dictionary?)
        """
        if original_notation == self.GENERIC_NOTE_NAME:
            return pitch_name
        if original_notation == self.LETTER_NAME:
            return self.generic_note_name_to_letter_name(pitch_name, prefer_sharps)[0]
        if original_notation == self.SOLFEGE_NAME:
            return self.generic_note_name_to_solfege(pitch_name, prefer_sharps)[0]
        if original_notation == self.CUSTOM_NAME:
            return self.generic_note_name_to_custom_note(pitch_name)[0]
        if original_notation == self.SCALAR_MODE_NUMBER:
            return self.generic_note_name_to_scalar_mode_number(pitch_name)[0]
        if original_notation == self.EAST_INDIAN_SOLFEGE_NAME:
            return self.generic_note_name_to_east_indian_solfege(pitch_name)[0]
        return pitch_name

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
            The distance in semitones (half steps) from the target
            pitch to the scalar pitch (If the target is higher than
            the scalar pitch, then distance > 0. If the target is
            lower than the scalar pitch then distance < 0. If the
            target matches a scale pitch, then distance = 0.)
        int
            error code (0 means success)
        """
        target = normalize_pitch(target)
        original_notation = self.get_pitch_type(target)
        prefer_sharps = "#" in target
        # The calculation is done in the generic note namespace
        target = self.convert_to_generic_note_name(target)[0]
        stripped_target, delta = strip_accidental(target)
        if stripped_target in self.note_names:
            i = self.note_names.index(stripped_target)
            i, delta_octave = self._map_to_semitone_range(i + delta, 0)
        target = self.note_names[i]

        # First look for an exact match.
        for i in range(self.get_mode_length()):
            if target == self.generic_scale[i]:
                return (
                    self._restore_format(target, original_notation, prefer_sharps),
                    i,
                    0,
                    0,
                )

        # Then look for the nearest note in the scale.
        if target in self.note_names:
            ti = self.note_names.index(target)
            # Look up for a note in the scale.
            distance = self.number_of_semitones
            n = 1
            for i in range(self.get_mode_length()):
                if i < ti + 1:
                    continue
                if self.note_names[i] in self.generic_scale:
                    closest_note = self.note_names[i]
                    distance = n
                    break
                n += 1
            # Look down.
            n = 1
            for i in range(ti):
                if self.note_names[ti - i] in self.generic_scale:
                    if n < distance:
                        return (
                            self._restore_format(
                                self.note_names[ti - i],
                                original_notation,
                                prefer_sharps,
                            ),
                            self.generic_scale.index(self.note_names[ti - i]),
                            -n,
                            0,
                        )
                    n += 1
            if distance < self.number_of_semitones:
                return (
                    self._restore_format(
                        closest_note, original_notation, prefer_sharps
                    ),
                    self.generic_scale.index(closest_note),
                    distance,
                    0,
                )

            print("Closest note to %s not found." % target)
            return (
                self._restore_format(target, original_notation, prefer_sharps),
                0,
                0,
                -1,
            )

        print("Note %s not found." % target)
        return self._restore_format(target, original_notation, prefer_sharps), 0, 0, -1

    def _prefer_sharps(self, key, mode):
        """
        Some keys prefer to use sharps rather than flats.
        """
        ks = "%s %s" % (key, mode)
        if ks in self.PREFER_SHARPS:
            return True
        """
        if mode in self.MODE_MAPPER:
            if isinstance(self.MODE_MAPPER[mode], str):
                ks = "%s %s" % (key, self.MODE_MAPPER[mode])
            elif key in self.MODE_MAPPER[mode]:
                ks = "%s %s" % (
                    self.MODE_MAPPER[mode][key][1],
                    self.MODE_MAPPER[mode][key][0],
                )
            else:
                if "#" in key:
                    key = self.EQUIVALENT_FLATS[key]
                else:
                    key = self.EQUIVALENT_SHARPS[key]
                ks = "%s %s" % (
                    self.MODE_MAPPER[mode][key][1],
                    self.MODE_MAPPER[mode][key][0],
                )
            return ks in self.PREFER_SHARPS
        """
        return False

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
        # return "%s %s [%s] [%s]" % (key, self.mode.upper(), hs, scale)
        return "%s %s [%s]" % (key, self.mode.upper(), scale)
