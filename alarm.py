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

import argparse
from ConfigParser import SafeConfigParser
import shlex
import subprocess
import timeit
import time
from os import system

def main(args):
	
	# Input arguments
	parser = argparse.ArgumentParser(description='pySleepWake alarm',prog='alarm.py')
	parser.add_argument("conf",help="configuration file")   
	args,unknown = parser.parse_known_args()

	# Read alarm conf file
	print "Reading conf file...",
	parser = SafeConfigParser()
	parser.read(args.conf)
	ip = parser.get('main', 'ip')
	mac = parser.get('main', 'mac')
	iface = parser.get('main', 'iface')
	npackets = int(parser.get('main', 'npackets'))
	pdel = float(parser.get('main', 'pdel'))*60.0
	print "OK"
	
	# commands
	args_tcp = shlex.split('tcpdump -i '+iface+' arp -c '+'1'+' -p'+' host '+ip)
	cmd_ping = "ping -c1 -w2 " + ip + " > /dev/null 2>&1"
	cmd_wake = 'etherwake -i '+iface+' '+mac
	
	# Wait for someone calls the server in the network
	pdel0 = timeit.default_timer() + pdel
	while True:
		tcpdump = subprocess.Popen(args_tcp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for row in iter(tcpdump.stdout.readline, b''):
			print row
			print row.find('packet')
			if row.find("1 packet captured") != -1:
				print "Someone is looking for the server..."
	
				# check if the server is online already
				if system(cmd_ping) != 0:
					print "It is not online..."
	
					# send magic packages if there is enough time delay
					# from last communication
					if timeit.default_timer() - pdel0 > 0.:
						for i in xrange(npackets):
							print "WAKE!"
							subprocess.call(cmd_wake,shell=True)
					else:
						delay = pdel0 - timeit.default_timer()
						print "Not enough time to wake it up :/ Waiting for %f s ..."%(delay)
						time.sleep(delay)
	
				else:
					pdel0 = timeit.default_timer() + pdel
					print "It is online... take it easy!"
	
	return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
