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
# This module contains all the reading functions for the lesgo module
# It will read the following files:
# lesgo.data - Data for lines, and planes to extract from CGNS file
# lesgo.compare - Data to compare from lesgo
# read_lesgo_data(): a function for reading the input file lesgo.data

from dataSample import linesClass, planeClass, fieldClass
import numpy as np

######################
def read_lesgo_data():
    '''
    This function reads in the lesgo.data file
    The file contains all the information with respect to
    which data to extract and how to plot it
    '''
    # Variables to be read from file
    # point1 - coordinates (x1,y1,z1)
    # point2 - coordinates (x2,y2,z2)
    # N - number of points in line

    # The file must always be in this location
    f=open('./lesgo.data','r')

    # List of line objects
    lines1D=[]

    # List of fields in domain
    fieldList=[]

    # List of planes
    planes=[]

    # Used to clip the domain
    clip=None

    # Initialize the flag to some bogus value
    flag='noflag'

    # Loop for all the lines in the file
    for line in f:
        # Ignore commented lines
        if not line.startswith('#') and line.strip():

            # Store the quantities given in the file to the dictionary
            line=line.strip()

            if line.split('=')[0]=='extract_1D_data':
                extract_1D_data=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='extract_2D_data':
                extract_2D_data=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='plot_1D_data':
                plot_1D_data=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='plot_2D_data':
                plot_2D_data=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='data_extract_location':
                data_extract_location=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='data_output_location':
                data_output_location=eval(line.split('=')[1])
                
            elif line.split('=')[0]=='plot_location':
                plot_location=eval(line.split('=')[1])

            elif line == 'fields:':
                flag = 'fields'

            elif line == '1D_data:':
                flag = '1D_data'

            elif line == '2D_data:':
                flag = '2D_data'

            elif line == 'avegare:':
                flag = 'average'

            # Read in the 1D data into lines class list
            elif flag == 'fields':
                try:
                    name= line.split(';')[0].strip()
                    File= line.split(';')[1].strip()
                    label= line.split(';')[2].strip()
                    # Declare field class object in list
                    fieldList.append( fieldClass(name=name, label=label, 
                                      File=File))
                    # Maximum and minimum values, if given
                    if len(line.split(';'))>3:
                        fieldList[-1].Min= float(line.split(';')[3])
                    if len(line.split(';'))>4:
                        fieldList[-1].Max= float(line.split(';')[4])
                except:
                    print( 'Error Reading fields')

            # Read in the 1D data into lines class list
            elif flag == '1D_data':
                #~ try:
                    name=line.split(';')[0]
                    p1=np.array(eval(line.split(';')[1]))
                    p2=np.array(eval(line.split(';')[2]))
                    N=eval(line.split(';')[3])
                    # Declare the class object as part of list
                    lines1D.append( linesClass( p1=p1, p2=p2, N=N, name=name,
                            extract_loc=data_extract_location, 
                            write_loc=data_output_location,
                            plot_loc=plot_location))
                #~ except:
                    #~ print('Error Reading data_1D')

            # Read in the 1D data into lines class list
            elif flag == '2D_data':
                try:
                    if line.split('=')[0].strip()=='clip':
                        clip=eval(line.split('=')[1])
                    else:
                        # Store the quantities given in the file to the dictionary
                        line=line.strip()
                        #~ print line
                        name_data=line.split(';')[0]
                        # The arguments passed as input to create class
                        args=line.split(';')[1]
                        # Create class object for plane
                        planes.append(eval('planeClass( ' + args + ' )') )
                        planes[-1].name=name_data
                        planes[-1].extract_loc=data_extract_location
                        planes[-1].write_loc=data_output_location
                        planes[-1].plot_loc=plot_location
                        if clip: planes[-1].clip=clip
                except:
                    print('Error Reading data_2D')

            elif flag == 'average':
                try:
                    print('Average')    
                except:
                    print('Could not perform averaging')

    result=[extract_1D_data, extract_2D_data, plot_1D_data, plot_2D_data,
            lines1D, planes, fieldList]
            
    return result
