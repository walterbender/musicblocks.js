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


def strip_accidental(pitch):
    """
    Remove an accidental and return the number of half steps that
    would have resulted from its application to the pitch

    Parameters
    ----------
    pitch : str
        Upper or lowecase pitch name with accidentals as ASCII or Unicode

    Returns
    -------
    str
        Normalized pitch name
    int
        Change in half steps represented by the removed accidental
    """
    if len(pitch) == 1:
        return pitch, 0
    # The ASCII versions
    if len(pitch) > 2 and pitch.endswith("bb"):
        return pitch.strip("bb"), -2
    if pitch.endswith("b"):
        return pitch.strip("b"), -1
    if pitch.endswith("#"):
        return pitch.rstrip("#"), 1
    if pitch.endswith("x"):
        return pitch.rstrip("x"), 2
    # And the Unicode versions...
    if pitch.endswith(DOUBLEFLAT):
        return pitch.strip(DOUBLEFLAT), -2
    if pitch.endswith(FLAT):
        return pitch.strip(FLAT), -1
    if pitch.endswith(SHARP):
        return pitch.rstrip(SHARP), 1
    if pitch.endswith(DOUBLESHARP):
        return pitch.rstrip(DOUBLESHARP), 2
    if pitch.endswith(NATURAL):
        return pitch.rstrip(NATURAL), 0
    # No accidentals were present.
    return pitch, 0


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
        Upper or lowecase pitch name with accidentals as ASCII or Unicode

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
        Upper or lowecase pitch name with accidentals as ASCII or Unicode

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
