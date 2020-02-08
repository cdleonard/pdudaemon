#!/usr/bin/python3

#  Copyright 2020 NXP
#  Author Leonard Crestez <leonard.crestez@nxp.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from pdudaemon.drivers.driver import PDUDriver
import serial
import time

import os
import logging
log = logging.getLogger("pdud.drivers." + os.path.basename(__file__))


class ICSE01xABase(PDUDriver):
    def __init__(self, hostname, settings):
        self.hostname = hostname
        self.settings = settings
        self.device = settings["device"]

        self.serial_port = None
        self.state = [False] * self.port_count

    def _open(self):
        self.serial_port = serial.serial_for_url(self.device,
            baudrate=9600, timeout=1)
        log.debug("open: %s", self.serial_port)
        self.serial_port.write(b'P')
        time.sleep(0.5)
        self.serial_port.write(b'Q')

    def handle(self, request, port_number):
        if port_number > self.port_count or port_number < 1:
            raise RuntimeError("Port should be in the range 1 - %d" % (self.port_count))

        if request == "on":
            self.state[port_number - 1] = True
        elif request == "off":
            self.state[port_number - 1] = False
        else:
            raise Exception("Unknown request %s" % (command,))

        byte = 0
        for i in range(self.port_count):
            if not self.state[i]:
                byte |= 1 << i

        try:
            if not self.serial_port:
                self._open()
            log.debug('write %#x', byte)
            self.serial_port.write([byte])
        except (serial.serialutil.SerialException, OSError) as e:
            log.error(e)
            # Will _open again next time:
            self.serial_port = None
            raise


    @classmethod
    def accepts(cls, drivername):
        return False


class ICSE012A(ICSE01xABase):
    """Supports ICSE012A

    See: http://www.icstation.com/icstation-micro-channel-relay-module-control-relay-module-icse012a-p-4012.html
    """
    port_count = 4

    @classmethod
    def accepts(cls, drivername):
        return drivername == 'ICSE012A'


class ICSE014A(ICSE01xABase):
    """Supports ICSE014A

    See http://www.icstation.com/icstation-channel-icse014a-micro-switch-relay-module-upper-computer-control-board-icse014a-p-5185.html
    """
    port_count = 8

    @classmethod
    def accepts(cls, drivername):
        return drivername == 'ICSE014A'
