# Copyright 2019 Andrzej Cichocki

# This file is part of Concern.
#
# Concern is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Concern is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Concern.  If not, see <http://www.gnu.org/licenses/>.

import re, sys

toplevel = re.compile(r'^\S')
anytext = re.compile(r'\S')
eol = '\n' # FoxDot uses API so anything is fine.
pilcrow = '\xb6'

def istoplevel(line):
    return toplevel.search(line) is not None

def hastext(line):
    return anytext.search(line) is not None

def getblock(text, first, last, pilcrow):
    lines = text.splitlines()
    max = len(lines) - 1
    first -= 1
    last -= 1
    if last > max:
        raise IndexError
    i = first
    while i < max and not hastext(lines[i]):
        if i >= last and istoplevel(lines[i + 1]):
            return '# Nothing to send.' + pilcrow + eol
        i += 1
    while last < max and not istoplevel(lines[last + 1]):
        last += 1
    while first < last and not hastext(lines[first]):
        first += 1
    while first and not istoplevel(lines[first]):
        first -= 1
    return eol.join(l for l in lines[first:last + 1] if hastext(l)) + pilcrow + eol

def readblock(pilcrow = pilcrow):
    return getblock(sys.stdin.read(), *map(int, sys.argv[1:]), pilcrow)
