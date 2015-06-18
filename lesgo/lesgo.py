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
'''
    Read lesgo.data and create the necessary data and plots from it
    The format read is CGNS which is read using the HDF5 library
    Many classes are contained which store and post-process the data
    Defines class for dealing with 1-D line samples
    linesClass: a class for storing and operating on 1D data
    plane.planeClass: a class for storing planes of data
    fieldClass: a class which stores the fields to be plotted
'''

import interpolation as intp
import numpy as np
import os
import h5py
import matplotlib.pyplot as plt
#~ from scipy.interpolate import griddata

#############################
# Data classes:
#############################

# 1D data
class linesClass(object):
    '''
    Holds the information for all the fields in the line plot
    '''

    def __init__(self, p1=None, p2=None, N=None, name=None,
                 extract_loc='../output', write_loc='./Data',
                 plot_loc='./plots'):
        '''
        The initialization of the class object
        p1 point 1 of the line
        p2 point 2 of the line
        N total number of line points
        name name of the line
        '''
        self.p1 = p1
        self.p2 = p2
        self.N = N
        self.name = name
        self.extract_loc = extract_loc
        self.write_loc = write_loc
        self.plot_loc = plot_loc
        self.data = {}  # The data list is a dictionary
        self.data['x'] = list(np.linspace(p1[0], p2[0], N))
        self.data['y'] = list(np.linspace(p1[1], p2[1], N))
        self.data['z'] = list(np.linspace(p1[2], p2[2], N))
        line_len = np.linalg.norm(p1-p2)  # line length
        self.data['arclength'] = list(np.linspace(0, line_len, N))

        # Create directories to write mean data
        if not os.path.exists(self.extract_loc):
            os.makedirs(self.extract_loc)
        if not os.path.exists(self.write_loc):
            os.makedirs(self.write_loc)
        if not os.path.exists(self.plot_loc):
            os.makedirs(self.plot_loc)
     
     @classmethod
     read(cls, read_loc=None):
         return linesClass()
        
    def addData(self, File=None, field=None):
        '''
        This will provide the data field
        '''
        # Point to the right location of the file
        File = self. extract_loc + '/' + File
        f = h5py.File(File, "r")
        path = '/Base/Zone/GridCoordinates/'

        x = np.asarray(f[path + 'CoordinateX/ data'])[0, 0, :]
        y = np.asarray(f[path + 'CoordinateY/ data'])[0, :, 0]
        z = np.asarray(f[path + 'CoordinateZ/ data'])[:, 0, 0]
        u = np.asarray(f['/Base/Zone/Solution/'+field+'/ data'])


        # Intetpolate the  value of the point from field
        dummy_array = []
        for i in xrange(0, self.N):
            u_i = [intp.interp3(x, y, z, u, self.data['x'][i],
                   self.data['y'][i], self.data['z'][i])][0]
            dummy_array.append(u_i)
        self.data[field] = dummy_array  # Save to object

        # Scipy interpolator (very slow)
        #~ x = np.asarray(f[path + 'CoordinateX/ data'])[:, :, :]
        #~ y = np.asarray(f[path + 'CoordinateY/ data'])[:, :, :]
        #~ z = np.asarray(f[path + 'CoordinateZ/ data'])[:, :, :]
        #~ u = np.asarray(f['/Base/Zone/Solution/'+field+'/ data']).flatten()
        #~ # Points where we want to interpolate
        #~ xi = zip(self.data['x'], self.data['y'], self.data['z'])
        #~ # Points where the data is
        #~ points = (x.flatten(), y.flatten(), z.flatten())
        #~ 
        #~ # Interpolate the data
        #~ self.data[field] = griddata(points, u, xi, method='linear')

    def writeData(self):
        '''
        Write the data to a file
        '''
        # Name of the data file
        name = self.name

        f = open(self.write_loc + '/' + name + '.dat', "w")

        N = self.N

        # The first fields to be written
        field_list = ['arclength', 'x', 'y', 'z']

        # The fields not wanted to be written
        unwanted = ['N', 'point1', 'point2']
        unwanted.extend(field_list)

        # The list of sorted arrays
        field_list.extend([x for x in sorted(self.data) if x not in unwanted])

        # Write data to file
        for val in (field_list):
            f.write('{0: >12}'.format(str(val)))
            f.write(' ')
        f.write('\n')
        for i in range(0, N):
            for val in (field_list):
                num = '{:3.8f}'.format(self.data[val][i])
                f.write('{0: >12}'.format(str(num)))
                f.write(' ')
            f.write('\n')
        f.close()

    def readData(self):
        '''
        Read the file stored and plot all of its quantities
        The output is a dictionary plot_data
        which contains all the fields
        '''
        # Open the file
        name = self.write_loc + '/' + self.name + '.dat'
        f = open(name, 'r')

        # Store the name of the fields for the dictionary
        fields = f.readline().split()

        self.data = dict(zip(fields, np.loadtxt(name, skiprows=1).T))

        #~ # Create the fields data as empyt lists
        #~ for field in fields:
            #~ self.data[field] = []
#~ 
        #~ # Loop for all the lines in the file and store
        #~ # the arrays for each field
        #~ for line in f:
            #~ for i, field in enumerate(fields):
                #~ self.data[field].append(line.split()[i])

    def plot(self, field, **parameters):
        '''
        Function for plotting
        field object from fieldClass
        '''

        plt.clf()
        x = self.data['arclength']
        plt.clf()
        y = self.data[field.name]
        plt.plot(x, y, '-o', color='black')
        plt.xlabel(r'$r/D$')
        plt.ylabel(field.label)
        plt.savefig(self.plot_loc + '/' + self.name + field.name + '.eps')
        plt.clf()


# Class for 2D data
class planeClass(object):
    '''
    Create a plane of data which is to be plotted

    Arguments:
    cutPlaneVector= points the normal vector to the plane
    pointPlane= A point in the plane
    maxVal= The maximum value for the legend
    minVal= The minimum value for the legend
    label= The text that goes in the legend
    upVector= The vector pointing up in the visualization

    functions:

    contour(self, file_name=):
    Creates the contour and stores it as an image

    '''

    def __init__(self, name=None, normal=None, dis=None,
                 extract_loc='../output', write_loc='./Data',
                 plot_loc='./plots'):
        '''
        The initialization of the class object
        '''
        # Name of the plane
        self.name = name

        # Plane coordinate distance
        self.dis = dis

        # Normal plane
        self.normal = normal

        self.extract_loc = extract_loc
        self.write_loc = write_loc
        self.plot_loc = plot_loc

        # Clipping of the domain
        self.clip = None
        # clip should be the limits in x, y, z
        # clip=[x0, x1, y0, y1, z0, z1]

        # Data coordinates
        self.x = None
        self.y = None
        self.z = None
        self.dx = None
        self.dy = None

        # The data from every field as a dictionary
        self.data = {}

        # Create directories to write/read data
        if not os.path.exists(self.extract_loc):
            os.makedirs(self.extract_loc)
        if not os.path.exists(self.write_loc):
            os.makedirs(self.write_loc)
        if not os.path.exists(self.plot_loc):
            os.makedirs(self.plot_loc)

    def extractData(self, fieldObj=None):
        '''
        This will provide the data field
        fieldObj is an object of the fieldClass
        '''
        field = fieldObj.name
        File = fieldObj.File

        print 'Extracting Contour data for', self.name, field

        # Point to the right location of the file
        File = self.extract_loc + '/' + File
        f = h5py.File(File, "r")

        # Load coordinates and field
        path = '/Base/Zone/GridCoordinates/'
        x_f = np.asarray(f[path + 'CoordinateX/ data'])[0, 0, :]
        y_f = np.asarray(f[path + 'CoordinateY/ data'])[0, :, 0]
        z_f = np.asarray(f[path + 'CoordinateZ/ data'])[:, 0, 0]
        u = np.asarray(f['/Base/Zone/Solution/' + field + '/ data'])

        # For the plane
        self.x = np.unique(np.clip(x_f, self.clip[0], self.clip[1]))
        self.y = np.unique(np.clip(y_f, self.clip[2], self.clip[3]))
        self.z = np.unique(np.clip(z_f, self.clip[4], self.clip[5]))
        # Create the plane points
        if self.normal == 'x':
            self.x = [self.dis]
            self.dx, self.dy = np.meshgrid(self.y, self.z)
            # Length of 2D array
            n1, n2 = len(self.y), len(self.z)
        if self.normal == 'y':
            self.y = [self.dis]
            self.dx, self.dy = np.meshgrid(self.x, self.z)
            # Length of 2D array
            n1, n2 = len(self.x), len(self.z)
        if self.normal == 'z':
            self.z = [self.dis]
            self.dx, self.dy = np.meshgrid(self.x, self.y)
            # Length of 2D array
            n1, n2 = len(self.x), len(self.y)

        self.data[field] = np.empty([n1, n2])

        if self.normal == 'x':
            x = self.x[0]
            for j, y in enumerate(self.y):
                for k, z in enumerate(self.z):
                    self.data[field][j, k] = intp.interp3(x_f, y_f, z_f,
                                                          u, x, y, z)
        if self.normal == 'y':
            y = self.y[0]
            for i, x in enumerate(self.x):
                for k, z in enumerate(self.z):
                    self.data[field][i, k] = intp.interp3(x_f, y_f, z_f,
                                                          u, x, y, z)
        if self.normal == 'z':
            z = self.z[0]
            for i, x in enumerate(self.x):
                for j, y in enumerate(self.y):
                    self.data[field][i, j] = intp.interp3(x_f, y_f, z_f,
                                                          u, x, y, z)

        np.savez(self.write_loc + '/' + self.name + field, self.dx, self.dy,
                 self.data[field])

    def readData(self, fieldObj=None):
        '''
        This will provide the data field
        fieldObj is an object of the fieldClass
        The data is read from numpy file (loadtxt)
        '''
        field = fieldObj.name
        npzfile = np.load(self.write_loc + '/' + self.name + field + '.npz')
        self.dx = npzfile['arr_0']
        self.dy = npzfile['arr_1']
        self.data[field] = npzfile['arr_2']

    #################################
    def contour(self, fieldObj=None):
        '''
        Create contour
        '''
        # Obtain information form field object
        field = fieldObj.name
        fMax = fieldObj.Max
        fMin = fieldObj.Min

        print 'Plotting Contour for', self.name, field

        for color in ['gray', 'hsv', 'spectral', 'gist_ncar', 'jet']:
            #~ matplotlib.rcdefaults()
            plt.clf()
            #~ print self.data[field].shape
            #~ print self.dx.shape, self.dy.shape

            # Adjust size of the figure
            #~ a,b=matplotlib.rcParams['figure.figsize']
            #~ mx=np.amax(self.dx)-np.amin(self.dx)
            #~ my=np.amax(self.dy)-np.amin(self.dy)
            #~ a*=max(mx,my)/mx
            #~ b*=max(mx,my)/my
            #~ matplotlib.rcParams['figure.figsize']=[a,b]
            #~ print a,b,matplotlib.rcParams['figure.figsize']

            plt.pcolormesh(self.dx, self.dy, self.data[field].T,
                           shading='gouraud',
                           cmap=plt.get_cmap(color), vmin=fMin, vmax=fMax)

            # Set the colorscale
            plt.gca().set_aspect('equal', adjustable='box')

            # Axis limits
            plt.xlim([np.amin(self.dx), np.amax(self.dx)])
            plt.ylim([np.amin(self.dy), np.amax(self.dy)])

            # Tick [ara,eters
            plt.tick_params(
                axis='both',        # changes apply to the x-axis
                which='both',       # both major and minor ticks are affected
                bottom='off',       # ticks along the bottom edge are off
                top='off',          # ticks along the top edge are off
                left='off',         # ticks along the left edge are off
                right='off',        # ticks along the right edge are off
                labelbottom='off',  # labels along the bottom edge are off
                labelleft='off')    # labels along the bottom edge are off

            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(plt.gca())
            cax = divider.append_axes("right", "2%", pad="3%")

            # Colorbar
            cb = plt.colorbar(cax=cax)

            # Number of labels
            m = ((np.amax(self.dy) - np.amin(self.dy)) /
                 (np.amax(self.dx) - np.amin(self.dx)))
            numLabel = int(3 * m + 3)

            # Set the numbe rof tick labels
            if fMax or fMin:
                cb.set_ticks(np.linspace(fMin, fMax, numLabel))

            #~ cb.set_label(label, rotation=0)

            # Figure attached to limits
            plt.tight_layout()

            plt.savefig(self.plot_loc + '/' + self.name + 
                        field + '-' + color + '.jpg', dpi=400)
            plt.close()

# Class for fields (velocity, pressure, etc)
class fieldClass(object):
    '''
    Stores the field with its information
    '''

    def __init__(self, name=None, label=None, File=None):
        # Name of the field
        self.name = name

        # String with label field
        self.label = label

        # File containing the field
        self.File = File

        # Maximum value of field
        self.Max = None

        # Minimum value of field
        self.Min = None


# Class for averaging
class averageClass(object):
    '''
    This class is intended to average in certain directions
    '''

    def __init__(self, plane=None, write_loc='./Data'):
        '''
        The initialization of the class object
        p1 point 1 of the line
        p2 point 2 of the line
        N total number of line points
        name name of the line
        '''
        self.plane = plane
        self.write_loc = write_loc

    def extractData(self, fieldObj=None):
        '''
        This will provide the data field
        fieldObj is an object of the fieldClass
        '''
        field = fieldObj.name
        File = fieldObj.File

        print(('Extracting Contour data for', self.name, field))

        # Point to the right location of the file
        File = '../output/' + File
        f = h5py.File(File, "r")

        # Load coordinates and field
        path = '/Base/Zone/GridCoordinates/'
        x_f = np.asarray(f[path + 'CoordinateX/ data'])[0, 0, :]
        y_f = np.asarray(f[path + 'CoordinateY/ data'])[0, :, 0]
        z_f = np.asarray(f[path + 'CoordinateZ/ data'])[:, 0, 0]
        u = np.asarray(f['/Base/Zone/Solution/' + field + '/ data'])

        # Perform numpy average
        if self.plane == 'x':
            uavg = np.average(np.average(u,axis=2),axis=1)
            np.savetxt(self.write_loc + '/avgx.dat', (x, u))

        if self.plane == 'y':
            uavg = np.average(np.average(u,axis=1),axis=1)
            np.savetxt(self.write_loc + '/avgy.dat', (y, u))
            
        if self.plane == 'z':
            uavg = np.average(np.average(u,axis=0),axis=1)
            np.savetxt(self.write_loc + '/avgz.dat', (z, u))


def caseData():
    '''
    This function will operate on a specific case data
    It is meant to be run in the case directory
    '''
    # Dependencies in this project

    # Read the input file 'lego.dat'
    [extract_1D_data, extract_2D_data, plot_1D_data, plot_2D_data,
     lines1D, planes, fieldList] = read_lesgo_data()

    # Extract all the data
    if extract_1D_data:
        print('Extracting and writing data')
        # Loop through all the line plots
        for line in lines1D:
            # Extract the field data
            for field in fieldList:
                line.addData(File=field.File, field=field.name)
            line.writeData()
        print('Done extracting and writing data')

    if plot_1D_data:
        print('Plotting Data')
        # Loop through all the line plots
        for line in lines1D:
            line.readData()  # Extract the field data
            for field in fieldList:  # Plot each field
                line.plot(field)
        print('Done plotting Data')

    if extract_2D_data:
        print('Extracting 2D data')
        for plane in planes:  # Extract each plane
            for field in fieldList:  # Extract each field
                plane.extractData(fieldObj=field)
        print('Done Extracting Data')

    if plot_2D_data:
        print('Plotting 2D Data')
        for plane in planes:  # Extract each plane
            for field in fieldList:  # Extract each field
                plane.readData(fieldObj=field)
                plane.contour(fieldObj=field)
        print('Done plotting 2D data')


######################
# Reading the input files
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

            elif line == 'average:':
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








