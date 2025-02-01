# Copyright (C) 2025 the baldaquin team.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Test suite for the plasduino project.
"""

from baldaquin import logger
from baldaquin.plasduino.protocol import AnalogReadout, DigitalTransition


def test_protocol():
    """Test the protocol.
    """
    readout = AnalogReadout(0xa2, 1, 1000, 255)
    logger.info(readout)
    logger.info(AnalogReadout.text_header('Something [a. u.]'))
    logger.info(readout.to_text())
    transition = DigitalTransition(0xa1, 1, 1000000)
    logger.info(transition)
    logger.info(DigitalTransition.text_header())
    logger.info(transition.to_text())
