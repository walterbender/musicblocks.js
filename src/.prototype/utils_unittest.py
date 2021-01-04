# -*- coding: utf-8 -*-
"""
Unit tests for musicutils
"""

# Copyright 2021 Walter Bender, Sugar Labs
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the The GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import unittest

import os
from musicutils import Temperament
from musicutils import KeySignature
from musicutils import normalize_pitch, display_pitch, strip_accidental

SHARP = "♯"
FLAT = "♭"
NATURAL = "♮"
DOUBLESHARP = "𝄪"
DOUBLEFLAT = "𝄫"


def round(f, d):
    i = f * d
    i += 0.5
    return float(int(i)) / d


class MusicUtilsTestCase(unittest.TestCase):
    def normalize_test(self):
        print("normalize_test")
        self.assertTrue(normalize_pitch("C" + SHARP) == "c#")
        self.assertTrue(display_pitch("c#") == "C" + SHARP)
        self.assertTrue(strip_accidental("c#")[0] == "c")
        self.assertTrue(strip_accidental("cbb")[0] == "c")
        self.assertTrue(strip_accidental("cbb")[1] == -2)
        self.assertTrue(strip_accidental("cb")[0] == "c")
        self.assertTrue(strip_accidental("cb")[1] == -1)
        self.assertTrue(strip_accidental("b")[0] == "b")
        self.assertTrue(strip_accidental("b")[1] == 0)

    def temperament_test(self):
        print("temperament_test")
        t = Temperament()
        self.assertEqual(t.get_name(), "equal")
        t.set_base_frequency(t.C0)
        self.assertEqual(t.get_base_frequency(), t.C0)
        self.assertEqual(t.get_number_of_octaves(), 8)
        f = t.get_freqs()
        self.assertEqual(round(f[21], 100), 55.0)  # A1
        self.assertEqual(len(t.get_note_names()), 12)

        t = Temperament(name="pythagorean")
        f = t.get_freqs()
        self.assertEqual(round(f[21], 100), 55.19)  # A1
        self.assertEqual(len(t.get_note_names()), 12)

        t = Temperament(name="just intonation")
        f = t.get_freqs()
        self.assertEqual(round(f[21], 100), 54.51)  # A1
        self.assertEqual(len(t.get_note_names()), 12)

        t = Temperament(name="quarter comma meantone")
        f = t.get_freqs()
        self.assertEqual(round(f[36], 100), 55.45)  # A1
        self.assertEqual(len(t.get_note_names()), 21)

        t = Temperament()
        t.generate_equal_temperament(24)
        f = t.get_freqs()
        self.assertEqual(round(f[42], 100), 55.0)  # A1
        self.assertEqual(len(t.get_note_names()), 24)

    def key_signature_test(self):
        print("key_signature_test")
        ks = KeySignature(mode="major", key="c")
        self.assertEqual(ks.closest_note("c")[0], "c")
        self.assertTrue(ks.note_in_scale("c"))
        self.assertEqual(ks.closest_note("f#")[0], "f")
        self.assertFalse(ks.note_in_scale("f#"))
        self.assertEqual(ks.closest_note("g#")[0], "g")
        self.assertFalse(ks.note_in_scale("g#"))
        self.assertEqual(ks.closest_note("cb")[0], "b")
        self.assertTrue(ks.note_in_scale("cb"))
        self.assertEqual(ks.closest_note("db")[0], "c")
        self.assertFalse(ks.note_in_scale("db"))

        # Test the scalar and semitone transforms and test for wrap around.
        self.assertEqual(ks.scalar_transform("c", 2)[0], "e")
        self.assertEqual(ks.scalar_transform("c", 2)[1], 0)  # no change to octave
        self.assertEqual(ks.scalar_transform("c#", 2)[0], "f")
        self.assertEqual(ks.semitone_transform("c", 2)[0], "d")
        self.assertEqual(ks.semitone_transform("c#", 2)[0], "d#")
        self.assertEqual(ks.semitone_transform("b", 1)[0], "c")
        self.assertEqual(ks.semitone_transform("b", 1)[1], 1)  # increment octave
        self.assertEqual(ks.semitone_transform("n3", 1)[0], "n4")
        self.assertEqual(ks.semitone_transform("n3#", 1)[0], "n5")
        self.assertEqual(ks.semitone_transform("n0", -1)[0], "n11")
        self.assertEqual(ks.semitone_transform("n0", -1)[1], -1)  # decrement octave
        self.assertEqual(ks.semitone_transform("n0b", -1)[0], "n10")
        self.assertEqual(ks.semitone_transform("n0b", -1)[1], -1)  # decrement octave
        self.assertEqual(ks.semitone_transform("n1b", -1)[0], "n11")
        self.assertEqual(ks.semitone_transform("n1b", -1)[1], -1)  # decrement octave
        self.assertEqual(ks.semitone_transform("n11x", 1)[0], "n2")
        self.assertEqual(ks.semitone_transform("n11x", 1)[1], 1)  # increment octave
        self.assertEqual(ks.closest_note("n10#")[0], "n11")
        self.assertEqual(ks.closest_note("n10x")[0], "n0")

        t = Temperament()
        self.assertEqual(
            int(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("a")[0], 4
                )
                + 0.5
            ),
            440,
        )

        ks = KeySignature(mode="chromatic", key="c")
        self.assertEqual(ks.scalar_transform("c", 2)[0], "d")
        self.assertEqual(ks.scalar_transform("c#", 2)[0], "eb")
        self.assertEqual(ks.semitone_transform("c", 2)[0], "d")
        self.assertEqual(ks.semitone_transform("c#", 2)[0], "d#")
        self.assertEqual(ks.semitone_transform("b", 1)[0], "c")

        t = Temperament(name="third comma meantone")
        ks = KeySignature(
            key="n0",
            number_of_semitones=t.get_number_of_semitones_in_octave(),
            mode=[2, 2, 1, 2, 2, 2, 7, 1],
        )
        self.assertEqual(len(ks.get_scale()), 8)
        self.assertEqual(ks.get_scale()[7], "n18")
        self.assertEqual(ks.closest_note("n12")[0], "n11")
        self.assertEqual(ks.scalar_transform("n5", 2)[0], "n9")
        self.assertEqual(ks.closest_note("n10#")[0], "n11")

        # Test equivalent mode mappings
        keys = [
            "c",
            "d",
            "e",
            "f",
            "g",
            "a",
            "b",
            "c#",
            "d#",
            "f#",
            "g#",
            "a#",
            "db",
            "eb",
            "gb",
            "ab",
            "bb",
        ]
        modes = [
            "dorian",
            "phrygian",
            "lydian",
            "mixolydian",
            "major",
            "minor",
            "locrian",
        ]
        for m in modes:
            for k in keys:
                ks = KeySignature(key=k, mode=m)
                # print(ks)

        # Test Solfege mapper
        ks = KeySignature(key="c", mode="major")
        self.assertEqual(len(ks.solfege_notes), 8)

        ks = KeySignature(key="c", mode="major pentatonic")
        self.assertEqual(len(ks.solfege_notes), 6)
        self.assertEqual(ks.solfege_notes[2], "me")
        self.assertEqual(ks.solfege_notes[3], "sol")

        ks = KeySignature(key="c", mode="minor pentatonic")
        self.assertEqual(len(ks.solfege_notes), 6)
        self.assertEqual(ks.solfege_notes[2], "fa")
        self.assertEqual(ks.solfege_notes[3], "sol")

        ks = KeySignature(key="c", mode="whole tone")
        self.assertEqual(len(ks.solfege_notes), 7)
        self.assertEqual(ks.solfege_notes[2], "me")
        self.assertEqual(ks.solfege_notes[3], "sol")

        ks = KeySignature(key="c", mode="chromatic")
        self.assertEqual(len(ks.solfege_notes), 13)
        self.assertEqual(ks.solfege_notes[2], "re")
        self.assertEqual(ks.solfege_notes[3], "meb")

        ks = KeySignature()
        self.assertEqual(ks.convert_to_generic_note_name("g")[0], "n7")
        self.assertEqual(ks.convert_to_generic_note_name("sol")[0], "n7")
        self.assertEqual(ks.convert_to_generic_note_name("5")[0], "n7")
        self.assertEqual(ks.convert_to_generic_note_name("pa")[0], "n7")
        self.assertEqual(ks.convert_to_generic_note_name("g#")[0], "n8")
        self.assertEqual(ks.convert_to_generic_note_name("sol#")[0], "n8")
        self.assertEqual(ks.convert_to_generic_note_name("5#")[0], "n8")
        self.assertEqual(ks.convert_to_generic_note_name("pa#")[0], "n8")

        ks.set_custom_note_names(
            ["charlie", "delta", "echo", "foxtrot", "golf", "alfa", "bravo"]
        )
        self.assertEqual(ks.convert_to_generic_note_name("golf")[0], "n7")
        self.assertEqual(ks.convert_to_generic_note_name("golf#")[0], "n8")

        self.assertEqual(ks.semitone_transform("g", 3)[0], "a#")
        self.assertEqual(ks.semitone_transform("n7", 3)[0], "n10")
        self.assertEqual(ks.semitone_transform("sol", 3)[0], "n10")
        self.assertEqual(ks.semitone_transform("5", 3)[0], "n10")
        self.assertEqual(ks.semitone_transform("pa", 3)[0], "n10")
        self.assertEqual(ks.semitone_transform("golf", 3)[0], "n10")

        self.assertEqual(ks.generic_note_name_to_solfege("n7")[0], "sol")
        self.assertEqual(ks.generic_note_name_to_solfege("n8")[0], "sol#")
        self.assertEqual(ks.generic_note_name_to_solfege("n9")[0], "la")
        self.assertEqual(ks.generic_note_name_to_east_indian_solfege("n7")[0], "pa")
        self.assertEqual(ks.generic_note_name_to_scalar_mode_number("n7")[0], "5")
        self.assertEqual(ks.generic_note_name_to_custom_note_name("n7")[0], "golf")

        t = Temperament()
        ks = KeySignature()
        ks.set_custom_note_names(
            ["charlie", "delta", "echo", "foxtrot", "golf", "alfa", "bravo"]
        )

        self.assertEqual(
            round(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("g")[0], 4
                ),
                100,
            ),
            392.03,
        )
        self.assertEqual(
            round(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("sol")[0], 4
                ),
                100,
            ),
            392.03,
        )
        self.assertEqual(
            round(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("5")[0], 4
                ),
                100,
            ),
            392.03,
        )
        self.assertEqual(
            round(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("pa")[0], 4
                ),
                100,
            ),
            392.03,
        )
        self.assertEqual(
            round(
                t.get_freq_by_generic_note_name_and_octave(
                    ks.convert_to_generic_note_name("golf")[0], 4
                ),
                100,
            ),
            392.03,
        )


if __name__ == "__main__":
    unittest.main()
