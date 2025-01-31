# dr14meter: compute the DR14 value of the given audio files
# Copyright (C) 2024  pe7ro
#
# dr14_t.meter: compute the DR14 value of the given audiofiles
# Copyright (C) 2011  Simone Riva
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

import numpy
import os
from dr14meter.audio_decoder import AudioDecoder


class AudioTrack:

    def __init__(self):
        self.Y = numpy.array([])
        self.Fs = 0
        self.channels = 0
        self.sample_width = 0
        self._ext = -1
        self._de = AudioDecoder()

    def time(self):
        return 1 / self.Fs * self.Y.shape[0]

    def get_file_ext_code(self):
        return self._ext

    def open(self, file_name):

        self.Y = numpy.array([])
        self.Fs = 0
        self.channels = 0

        if not (os.path.exists(file_name)):
            return False

        res_f = self._de.read_track_new(file_name, self)
        self._ext = self._de.get_file_ext_code()

        return res_f
