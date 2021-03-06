#!/usr/bin/env python
################################################################################
## Written by:
##
##   Luis 'Tony' Martinez <tony.mtos@gmail.com> (Johns Hopkins University)
##
##   Copyright (C) 2012-2013, Johns Hopkins University
##
##   This file is part of Lesgo
##
##   Lesgo is free software: you can redistribute it
##   and/or modify it under the terms of the GNU General Public License as
##   published by the Free Software Foundation, either version 3 of the
##   License, or (at your option) any later version.
##
##   Lesgo is distributed in the hope that it will be
##   useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public License
##   along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
##
################################################################################
# This file is intended to test the lesgo module
#~ from nose.tools import *
from lesgo import lesgo

# Get information for the case
lesgo.caseData(filename='lesgo.data')
