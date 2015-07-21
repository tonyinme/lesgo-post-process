################################################################################
## Written by:
##
##   Luis 'Tony' Martinez <tony.mtos@gmail.com> (Johns Hopkins University)
##
##   Copyright (C) 2012-2015, Johns Hopkins University
##
##   This file is part of Lesgo-post-process
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
BEMClass - This class will read and write information from the
actuator turbine model in LESGO
'''

# Standard Python imports
import numpy as np
import os


# Class for averaging BEM data and writing it
class BEMClass(object):
    '''
    This class is intended to deal with BEM data from the
    actuator turbine model (ATM)
    '''

    def __init__(self, field=None, write_loc='./Data', read_loc='./'):
        '''
        The initialization of the class object
        field - the BEM field (lift, drag, etc)
        '''
        self.field = field
        self.write_loc = write_loc
        self.read_loc = read_loc

    def readBEM(self, avgperc=0.5):
        '''
        This will read a file from the actuator turbine model
        containing quantities along the blade such as lift, drag, etc

        avgperc is the percentage of the file to average (from the end)
        '''
        nr = 2  # This is from which column to start reading

        # Load the file
        y = np.loadtxt(self.read_loc + '/' + self.field, skiprows=1)

        # Establish from what point to average
        n = np.shape(y)[0] * avgperc

        # Average
        self.y = y[-n:, nr:].mean(axis=0)

        # Load the blade data
        self.x = np.loadtxt(self.read_loc + '/blade', skiprows=1)[-1, nr:]

    def writeBEM(self):
        '''
        This function will write the averaged data
        '''
        # Create directories to save plots
        if not os.path.exists(self.write_loc):
            os.makedirs(self.write_loc)

        # Open the file
        f = open(self.write_loc + '/avg_' + self.field + '.dat', "w")

        # Write file header
        f.write('{0: >12}'.format('r/R'))
        f.write('{0: >12}'.format(self.field))
        f.write('\n')

        # Write each line
        for i in range(len(self.x)):
            num = '{:3.8f}'.format(self.x[i])
            f.write('{0: >12}'.format(str(num)))
            f.write(' ')
            num = '{:3.8f}'.format(self.y[i])
            f.write('{0: >12}'.format(str(num)))
            f.write('\n')
        f.close()


def powerAndThrust(read_loc, avgperc=0.5):
    '''
    Average power
    read_loc - The location where to read the files from
    '''
    # Load the file
    p = np.loadtxt(read_loc + '/power', skiprows=1)
    t = np.loadtxt(read_loc + '/thrust', skiprows=1)

    # Establish from what point to average
    n = np.shape(p)[0] * avgperc

    nr = 1  # This is which column to average

    # Average
    p = p[-n:, nr].mean(axis=0)
    t = t[-n:, nr].mean(axis=0)

    f = open(read_loc + '/Data/avg_power_thrust.dat', "w")
    # Write file header
    f.write('{0: >12}'.format('power'))
    f.write('{0: >12}'.format('thrust'))
    f.write('\n')
    num = '{:3.8f}'.format(p)
    f.write('{0: >12}'.format(str(num)))
    f.write(' ')
    num = '{:3.8f}'.format(t)
    f.write('{0: >12}'.format(str(num)))
    f.write('\n')

    f.close()


def caseData(cases):
    '''
    This function will read all the data and calculate the mean values
    cases - a list of directories for each case
    '''
    # List of variables to plot
    ls = ['alpha', 'Cd', 'Cl', 'drag', 'lift', 'Vaxial', 'Vrel', 'Vtangential']

    for case in cases:
        for field in ls:
            bem = BEMClass(field=field, write_loc=case + '/Data', read_loc=case)
            bem.readBEM()
            bem.writeBEM()
        powerAndThrust(case)