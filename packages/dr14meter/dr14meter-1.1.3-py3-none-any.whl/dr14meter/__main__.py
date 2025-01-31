# dr14meter: compute the DR14 value of the given audio files
# Copyright (C) 2024  pe7ro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# __all__ = ["main"]

import sys

# from src import dr14meter

if (__package__ is None or len(__package__) == 0) and not getattr(sys, 'frozen', False):
    import pathlib
    path = pathlib.Path(__file__).resolve()
    sys.path.insert(0, str(path.parent.parent))

import dr14meter.dr14_tmeter as dr14
# import .dr14meter


def main():
    """Entry point for the application script"""
    dr14.main()


if __name__ == '__main__':
    main()


