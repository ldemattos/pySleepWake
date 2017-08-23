#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  log.py
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

import logging

def setup(filename,log_level):
	
	# instantiating logging object
	logger = logging.getLogger(__name__)
	logger.setLevel(log_level)
	
	# create a file handler
	handler = logging.FileHandler('log/sleep.log')
	handler.setLevel(log_level)
	
	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	
	# add the handlers to the logger
	logger.addHandler(handler)
	
	return(logger)
