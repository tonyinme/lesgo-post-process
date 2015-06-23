################################################################################
## Written by:
##
##   Luis 'Tony' Martinez <tony.mtos@gmail.com> (Johns Hopkins University)
##
##   Copyright (C) 2012-2015, Johns Hopkins University
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
'''
    This will store all the reading functions
    for the lesgo module
'''
import numpy as np

def readData(name=None):
    '''
    Read the file stored 
    This file needs the proper format
    '''
    # Open the file
    f = open(name, 'r')

    # Store the name of the fields for the dictionary
    fields = f.readline().split()

    data = dict(zip(fields, np.loadtxt(name, skiprows=1).T))

    return data

def readNPZData(xname='arr_0', yname='arr_1', field='arr_2', fname=None):
    '''
    Reads an NPZ file written by the lesgo module
    xname = string name for x coordinate
    yname = string name for y coordinate
    field = the field to be read
    fname = file name
    '''
    fname=fname
    field = field
    npzfile = np.load(fname)
    x = npzfile['arr_0']
    y = npzfile['arr_1']
    d = npzfile['arr_2']

    return [x, y, d]










