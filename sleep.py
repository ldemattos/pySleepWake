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
import time

def main(args):

    # Read server conf file
    print "Reading conf file...",
    parser = SafeConfigParser()
    parser.read(sys.argv[1])
    TxRx_rate = float(parser.get('sleep', 'TxRx_rate'))
    tWin = float(parser.get('sleep', 'twin'))
    tdel = float(parser.get('sleep', 'tdel'))
    iface = parser.get('sleep', 'iface')
    print "OK"

    # Initialize time vector
    winlen = int(round(tWin/tdel))
    rx_win = [TxRx_rate*winlen for i in xrange(winlen)]
    tx_win = [TxRx_rate*winlen for i in xrange(winlen)]

    # commands
    cmd_rx = 'cat /sys/class/net/'+iface+'/statistics/rx_bytes'
    args_rx = shlex.split(cmd_rx)
    cmd_tx = 'cat /sys/class/net/'+iface+'/statistics/tx_bytes'
    args_tx = shlex.split(cmd_tx)
    cmd_suspend = 'systemctl suspend'

    first_loop = 1
    while True:

        if first_loop == 1:
            rx_ref = subprocess.Popen(args_rx, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            rx_ref = int((rx_ref.stdout.readline()).strip())

            tx_ref = subprocess.Popen(args_tx, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            tx_ref = int((tx_ref.stdout.readline()).strip())

            i = 0
            first_loop = 0

        else:
            # read received bytes
            rx = subprocess.Popen(args_rx, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            rx_val = int(rx.stdout.readline().strip())
            rx_win[i] = (rx_val-rx_ref)/1000.0/(tdel*60.0)

            # read transceived bytes
            tx = subprocess.Popen(args_tx, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            tx_val = int(tx.stdout.readline().strip())
            tx_win[i] = (tx_val-tx_ref)/1000.0/(tdel*60.0)

            print "rx: ",
            print rx_win
            print "tx: ",
            print tx_win

            # compute the windows' averages
            rx_avg = 0.0
            tx_avg = 0.0
            j = 0
            for x in rx_win:
                rx_avg += x
                tx_avg += tx_win[j]
                j+=1

            rx_avg = rx_avg / winlen
            tx_avg = tx_avg / winlen

            print tx_avg
            print rx_avg

            # Update references
            rx_ref = rx_val
            tx_ref = tx_val

            # Update counter
            if i == winlen-1:
                i=0
            else:
                i+=1

            # Check avegerages
            if rx_avg < TxRx_rate and tx_avg < TxRx_rate:
                # Reset variables before suspending
                fist_loop = 1
                rx_win = [TxRx_rate*winlen for i in xrange(winlen)]
                tx_win = [TxRx_rate*winlen for i in xrange(winlen)]
                subprocess.call(cmd_suspend,shell=True)

        # Delay the next measureament
        time.sleep(60.*tdel)

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
