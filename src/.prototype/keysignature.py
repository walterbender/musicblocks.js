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

from musicutils import strip_accidental, normalize_pitch, display_pitch

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

    # This notation only applies to temperaments with 12 semitones.
    PITCH_LETTERS = ["c", "d", "e", "f", "g", "a", "b"]
    SCALAR_MODE_NUMBERS = ["1", "2", "3", "4", "5", "6", "7"]
    SOLFEGE_NAMES = ["do", "re", "me", "fa", "sol", "la", "ti"]
    EAST_INDIAN_NAMES = ["sa", "re", "ga", "ma", "pa", "dha", "ni"]

    # These defintions are only relevant to equal temperament.
    NOTES_SHARP = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    NOTES_FLAT = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "bb", "b"]

    # TODO:
    # We need to think about how to capture the notion that C Major
    # Pentatonic should feel like G Major (and use G Major in its score.
    # Are there preferences for chromatic? for octotonic? etc.
    MODE_MAPPER = {
        "ionian": "major",
        "dorian": {
            "c": ["major", "bb"],
            "d": ["major", "c"],
            "e": ["major", "d"],
            "f": ["minor", "c"],
            "g": ["major", "f"],
            "a": ["major", "g"],
            "b": ["major", "a"],
            "c#": ["major", "b"],
            "d#": ["major", "c#"],
            "f#": ["major", "e"],
            "g#": ["major", "f#"],
            "a#": ["major", "ab"],
            "db": ["minor", "ab"],
            "eb": ["minor", "bb"],
            "gb": ["minor", "c#"],
            "ab": ["minor", "eb"],
            "bb": ["minor", "f"],
        },
        "phrygian": {
            "c": ["major", "ab"],
            "d": ["major", "bb"],
            "e": ["major", "c"],
            "f": ["major", "db"],
            "g": ["minor", "c"],
            "a": ["major", "f"],
            "b": ["major", "g"],
            "c#": ["major", "a"],
            "d#": ["major", "b"],
            "f#": ["major", "d"],
            "g#": ["major", "e"],
            "a#": ["major", "f#"],
            "db": ["major", "a"],
            "eb": ["minor", "ab"],
            "gb": ["major", "d"],
            "ab": ["major", "e"],
            "bb": ["minor", "eb"],
        },
        "lydian": {
            "c": ["major", "g"],
            "d": ["major", "a"],
            "e": ["major", "b"],
            "f": ["major", "c"],
            "g": ["major", "d"],
            "a": ["major", "e"],
            "b": ["major", "f#"],
            "c#": ["major", "ab"],
            "d#": ["major", "bb"],
            "f#": ["major", "c#"],
            "g#": ["minor", "c"],
            "a#": ["major", "bb"],
            "db": ["minor", "c"],
            "eb": ["minor", "g"],
            "gb": ["minor", "bb"],
            "ab": ["minor", "c"],
            "bb": ["minor", "d"],
        },
        "mixolydian": {
            "c": ["major", "f"],
            "d": ["major", "g"],
            "e": ["major", "a"],
            "f": ["major", "bb"],
            "g": ["major", "c"],
            "a": ["major", "d"],
            "b": ["major", "e"],
            "c#": ["major", "f#"],
            "d#": ["major", "ab"],
            "f#": ["major", "b"],
            "g#": ["major", "f"],
            "a#": ["minor", "c"],
            "db": ["minor", "eb"],
            "eb": ["minor", "f"],
            "gb": ["minor", "ab"],
            "ab": ["minor", "bb"],
            "bb": ["minor", "c"],
        },
        "locrian": {
            "c": ["major", "db"],
            "d": ["minor", "c"],
            "e": ["major", "f"],
            "f": ["major", "gb"],
            "g": ["major", "ab"],
            "a": ["major", "bb"],
            "b": ["major", "c"],
            "c#": ["major", "d"],
            "d#": ["minor", "c#"],
            "f#": ["major", "g"],
            "g#": ["major", "a"],
            "a#": ["major", "b"],
            "db": ["major", "d"],
            "eb": ["minor", "db"],
            "gb": ["major", "f#"],
            "ab": ["minor", "gb"],
            "bb": ["minor", "ab"],
        },
        "aeolian": "minor",
        "natural minor": "minor",
        "harmonic minor": "minor",
        "major": "major",
        "minor": "minor",
    }

    PREFER_SHARPS = [
        "g major",
        "e minor",
        "d major",
        "b minor",
        "e major",
        "c# minor",
        "db minor",
        "b major",
        "g# minor",
        "e minor",
        "g major",
        "e minor",
        "a major",
        "f# minor",
        "gb minor",
        "c# major",
        "a# minor",
        "f# major",
        "d minor",
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

        # Define generic note names that map to temperament.
        self.note_names = []
        for i in range(self.number_of_semitones):
            self.note_names.append("n%d" % i)
        # Solfege notes may be available
        self.solfege_notes = []
        # East Indian Solfege notes may be available
        self.east_indian_solfege_notes = []
        # Scalar Mode numbers may be available
        self.scalar_mode_numbers = []
        # Custom note names may also be available
        self.custom_note_names = []

        # We handle 12-semitone temperaments differently since they
        # can use letter name and predefined modes.
        if self.number_of_semitones == 12:
            if isinstance(mode, str):
                self.mode = mode.lower()
                # Some mode names imply a specific key.
                if mode in self.MAQAM_KEY_OVERRIDES:
                    # Override the key.
                    key = self.MAQAM_KEY_OVERRIDES[mode]
                    mode = "maqam"
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
        if self.number_of_semitones == 12:
            self._assign_solfege_note_names()
            self._assign_east_indian_solfege_note_names()
            self._assign_scalar_mode_numbers()

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
        # Maybe it is already a generic name.
        if pitch_name in self.note_names:
            return pitch_name, 0
        if self.number_of_semitones != 12:
            print("Cannot convert %s to a generic note name." % pitch_name)
            return "", -1

        # Look for a letter name, e.g., g# or ab
        if "#" in pitch_name and pitch_name in self.NOTES_SHARP:
            return self.note_names[self.NOTES_SHARP.index(pitch_name)], 0
        if pitch_name in self.NOTES_FLAT:
            return self.note_names[self.NOTES_FLAT.index(pitch_name)], 0

        # Look for a Solfege name
        note_name = self._name_converter(pitch_name, self.solfege_notes)
        if note_name is not None:
            return note_name, 0
        # Look for a Custom name
        if len(self.custom_note_names) > 0:
            note_name = self._name_converter(pitch_name, self.custom_note_names)
            if note_name is not None:
                return note_name, 0
        # Look for a Scalar mode number
        note_name = self._name_converter(pitch_name, self.scalar_mode_numbers)
        if note_name is not None:
            return note_name, 0
        # Look for a East Indian Solfege name
        note_name = self._name_converter(pitch_name, self.east_indian_solfege_notes)
        if note_name is not None:
            return note_name, 0

        print("Pitch name %s not found." % pitch_name)
        return "", -1

    def generic_note_name_to_letter_name(self, note_name, prefer_sharps=True):
        """
        Convert from a generic note name as defined by the temperament
        to a letter name used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """
        note_name = normalize_pitch(note_name)
        # Maybe it is already a letter name?
        if note_name in self.NOTES_SHARP:
            return note_name, 0
        if note_name in self.NOTES_FLAT:
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

    def generic_note_name_to_solfege(self, note_name):
        """
        Convert from a generic note name as defined by the temperament
        to a solfege note used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        return self._convert_from_note_name(note_name, self.solfege_notes)

    def generic_note_name_to_east_indian_solfege(self, note_name):
        """
        Convert from a generic note name as defined by the temperament
        to an East Indian solfege note used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        return self._convert_from_note_name(note_name, self.east_indian_solfege_notes)

    def generic_note_name_to_scalar_mode_number(self, note_name):
        """
        Convert from a generic note name as defined by the temperament
        to a scalar mode number used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        return self._convert_from_note_name(note_name, self.scalar_mode_numbers)

    def generic_note_name_to_custom_note_name(self, note_name):
        """
        Convert from a generic note name as defined by the temperament
        to a custom_note_name used by 12-semitone temperaments.
        NOTE: Only for temperaments with 12 semitones.
        """

        return self._convert_from_note_name(note_name, self.custom_note_names)

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
        mode_length = self.get_mode_length()
        delta_octave = 0
        if self.number_of_semitones == 12:
            if starting_pitch in self.NOTES_SHARP:
                i = self.NOTES_SHARP.index(starting_pitch)
                i += number_of_half_steps
                i, delta_octave = self._map_to_semitone_range(i, delta_octave)
                return self.NOTES_SHARP[i], delta_octave, 0
            elif starting_pitch in self.NOTES_FLAT:
                i = self.NOTES_FLAT.index(starting_pitch)
                i += number_of_half_steps
                i, delta_octave = self._map_to_semitone_range(i, delta_octave)
                return self.NOTES_FLAT[i], delta_octave, 0
            else:
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

        # First, we need to find the closest note to our starting
        # pitch.
        closest, closest_index, distance, e = self.closest_note(starting_pitch)
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
        new_note = self.scale[normalized_index]

        # We need to keep track of whether or not we crossed C, which
        # is the octave boundary.
        if new_index < 0:
            delta_octave -= 1

        # De we need to take into account the distance from the
        # closest scalar note?
        if distance == 0:
            return new_note, delta_octave

        # Accidentals for non-12-semitone temperaments are removed
        # inside closest_note.
        if self.number_of_semitones != 12:
            i += distance
            i, delta_octave = self._map_to_scalar_range(i, delta_octave)
            return self.note_names[i], delta_octave

        if "#" in starting_pitch:
            i = self.NOTES_SHARP.index(new_note)
        else:
            i = self.NOTES_FLAT.index(new_note)
        i += distance
        i, delta_octave = self._map_to_scalar_range(i, delta_octave)

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
            The distance in semitones (half steps) from the target
            pitch to the scalar pitch (If the target is higher than
            the scalar pitch, then distance > 0. If the target is
            lower than the scalar pitch then distance < 0. If the
            target matches a scale pitch, then distance = 0.)
        int
            error code (0 means success)
        """
        target = normalize_pitch(target)
        if self.number_of_semitones == 12:
            original_notation = None
            convert_to_generic_note_name = False
            # TODO: Figure out what notation is used here.
            if target[0] == "n":
                stripped_target, delta = strip_accidental(target)
                if stripped_target in self.note_names:
                    i = self.note_names.index(stripped_target)
                    i, delta_octave = self._map_to_semitone_range(i + delta, 0)
                target = self.generic_note_name_to_letter_name(
                    self.note_names[i], prefer_sharps="#" in target
                )[0]
                convert_to_generic_note_name = True
                original_notation = "note name"

            # First, try to find an exact match
            for i in range(self.get_mode_length()):
                if target == self.scale[i]:
                    if convert_to_generic_note_name:
                        target = self.convert_to_generic_note_name(target)[0]
                    return target, i, 0, 0
            # Next, see if one of the equivalent notes matches
            for i in range(self.get_mode_length()):
                if target in self.EQUIVALENTS:
                    for k in self.EQUIVALENTS[target]:
                        if k == self.scale[i]:
                            if convert_to_generic_note_name:
                                return (
                                    self.convert_to_generic_note_name(self.scale[i])[0],
                                    i,
                                    0,
                                    0,
                                )
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
                if convert_to_generic_note_name:
                    closest = self.convert_to_generic_note_name(closest)[0]
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
                    if convert_to_generic_note_name:
                        closest = self.convert_to_generic_note_name(closest)[0]
                    return closest, closest_idx, closest_distance, -1

                if abs(i2 - i1) < abs(closest_distance):
                    closest = self.scale[i]
                    closest_idx = i
                    closest_distance = i2 - i1
                if abs(i2 + self.number_of_semitones - i1) < abs(closest_distance):
                    closest = self.scale[i]
                    closest_idx = i
                    closest_distance = i2 + self.number_of_semitones - i1

            if convert_to_generic_note_name:
                closest = self.convert_to_generic_note_name(closest)[0]
            return closest, closest_idx, closest_distance, 0

        # Handle temperaments with more than 12 semitones separately.
        stripped_target, delta = strip_accidental(target)
        if stripped_target in self.note_names:
            i = self.note_names.index(stripped_target)
            i, delta_octave = self._map_to_semitone_range(i + delta, 0)
        target = self.note_names[i]

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

    def _prefer_sharps(self, key, mode):
        """
        Some keys prefer to use sharps rather than flats.
        """
        if mode in self.MODE_MAPPER:
            if isinstance(self.MODE_MAPPER[mode], str):
                ks = "%s %s" % (key, self.MODE_MAPPER[mode])
            else:
                ks = "%s %s" % (
                    self.MODE_MAPPER[mode][key][1],
                    self.MODE_MAPPER[mode][key][0],
                )
            return ks in self.PREFER_SHARPS
        return False

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
        if self._prefer_sharps(self.key, self.mode):
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
            if not self._prefer_sharps(self.key, self.mode) and "#" in self.key:
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
