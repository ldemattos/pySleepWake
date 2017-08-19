#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sleep.py
#
# Copyright (C) 2017 Leonardo M. N. de Mattos <l@mattos.eng.br>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ConfigParser import SafeConfigParser
import shlex
import subprocess

def main(args):

    # Read server conf file
    print "Reading conf file...",
    parser = SafeConfigParser()
    parser.read(sys.argv[1])
    ip = parser.get('main', 'ip')
    mac = parser.get('main', 'mac')
    iface = parser.get('main', 'iface')
    npackets = int(parser.get('main', 'npackets'))
    print "OK"

    # commands
    cmd_tcp = 'tcpdump -i '+iface+' -c '+'1'+' -p'+' host '+ip
    args_tcp = shlex.split(cmd_tcp)
    cmd_ping = 'ping '+ip+' -c1'
    args_ping = shlex.split(cmd_ping)
    cmd_wake = 'etherwake -i '+iface+' '+mac

    # Wait for someone calls the server in the network
    while True:
        tcpdump = subprocess.Popen(args_tcp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for row in iter(tcpdump.stdout.readline, b''):
            print row
            print row.find('packet')
            if row.find("1 packet captured") != -1:
                print "Someone is looking for the server..."

                # check if the server is online already
                ping = subprocess.Popen(args_ping, stdout=subprocess.PIPE)
                for row in iter(ping.stdout.readline, b''):
                    print row
                    if row.find("1 packets transmitted, 0 received") != -1:
                        print "It is not online..."

                        # send magic packages
                        for i in xrange(npackets):
                            print "WAKE!"
                            subprocess.call(cmd_wake,shell=True)

                    else:
                        print "It is online... take it easy!"

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
