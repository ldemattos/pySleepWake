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
from os.path import dirname
from os.path import realpath
import sys
sys.path.insert(0, dirname(realpath(sys.argv[0]))+'/src')
import log

def main(args):

	# Input arguments
	parser = argparse.ArgumentParser(description='pySleepWake alarm',prog='alarm.py')
	parser.add_argument("conf",help="configuration file")
	args,unknown = parser.parse_known_args()

	# Read conf file
	parser = SafeConfigParser()
	parser.read(args.conf)

	# Setup log
	logger = log.setup(parser.get('log','log_file'),int(parser.get('log','log_level')))

	# Read alarm conf file
	logger.info("Reading conf file...")
	ip = parser.get('main', 'ip')
	mac = parser.get('main', 'mac')
	iface = parser.get('main', 'iface')
	npackets = int(parser.get('main', 'npackets'))
	pdel = float(parser.get('main', 'pdel'))*60.0
	blacklist = parser.get('main', 'blacklist').replace(' ','').split(',')
	logger.info("...OK")

	# commands
	args_tcp = shlex.split('tcpdump -i '+iface+' arp -c '+'1'+' -p'+' dst '+ip)
	cmd_ping = "ping -c1 -w2 " + ip + " > /dev/null 2>&1"
	cmd_wake = 'etherwake -i '+iface+' '+mac

	# Wait for someone calls the server in the network
	pdel0 = timeit.default_timer() + pdel
	while True:
		tcpdump = subprocess.Popen(args_tcp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for row in iter(tcpdump.stdout.readline, b''):

			# acquire the poker
			if row.find("who-has") != -1:
				poker = (row.split()[6])[:-1]
				logger.debug("%s is looking for the server..."%(poker))
				
				# check logic conditions
				blist = not poker in blacklist
				ping = (system(cmd_ping) != 0)
				deltat = timeit.default_timer() - pdel0
				
				# Check for all conditions
				if all([blist, ping, deltat > 0.0]):				
					for i in xrange(npackets):
						logger.info("Waking up the server... Requested by %s"%(poker))
						subprocess.call(cmd_wake,shell=True)
							
					pdel0 = timeit.default_timer() + pdel						
						
				else:		
					logger.debug("One or more wakeup conditions weren't met: blist=%s,ping=%s,Dt=%f"%(blist,ping,deltat))
					if deltat > 0.:
						time.sleep(delay)			

	return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
