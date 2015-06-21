#!/usr/bin/python2.7
# This will read in a CGNS file and convert it to a vapor VDF fromat
# It needs to call vapor functions so these need to bet set properly
# As environment variables
# ./cgns_to_vdf file.cgns

import os
from array import *
import h5py
import numpy as np
import sys
import struct

def main():

    print 'Converting files: '+ str(sys.argv[1:])

    # Read the CGNS file
    for file_name in sys.argv[1:]:
        convert_cgns_to_vdf( file_name )






def create_vdf( file_name, variables ):
    ''' 
    Write u array to a binary file and 
    use it to create VFD file from the 
    Vapor (NCAR) commands
    '''
    #~ u.astype('float32').tofile(file_name)

    # minL used to scale dimension so the start at 1.0
    minL=min([L_x,L_y,L_z])
    cmd1=['vdfcreate -dimension '+str(N_x)+'x'+str(N_y) +'x'+str(N_z)+
        ' -level 0 -extents 0:0:0:'+str(L_x/minL)+
        ':'+str(L_y/minL)+':'+str(L_z/minL)+
        ' -vars3d '+':'.join(variables)+' '+ file_name+'.vdf']
    os.system(cmd1[0])
    print cmd1[0]

def populate_vdf( file_name, var ):
    ''' 
    Populat the VDF file using
    the Vapor (NCAR) commands
    '''
    cmd2=['raw2vdf -varname '+ var +' '+
           file_name+'.vdf ' + var]
    os.system(cmd2[0])
    print cmd2[0]
    
def convert_cgns_to_vdf(file_name):
    '''
    Will read CGNS file and store as a numpy array u
    Then calls the create VDF subroutines to create the vdf files
    '''
    # Read the cgns file    
    f= h5py.File( file_name , "r")
    
    x_f = np.asarray(f['/Base/Zone/GridCoordinates/CoordinateX/ data'])[0,0,:]
    y_f = np.asarray(f['/Base/Zone/GridCoordinates/CoordinateY/ data'])[0,:,0]
    z_f = np.asarray(f['/Base/Zone/GridCoordinates/CoordinateZ/ data'])[:,0,0]
    global L_x,L_y,L_z,N_x,N_y,N_z
    L_x=max(x_f)
    L_y=max(y_f)
    L_z=max(z_f)    
    N_x=len(x_f)
    N_y=len(y_f)
    N_z=len(z_f)    

    # Name for the vapor and vdf files
    fname=file_name.replace('.cgns', '').replace('.', '').replace('/', '')
    create_vdf( fname, f['/Base/Zone/Solution/'] )

    # Loop through all variables in file and create the VDF
    for sol in f['/Base/Zone/Solution/']:
        u = np.asarray(f['/Base/Zone/Solution/'+sol+'/ data'])
        write_binary( sol , u)
        populate_vdf( fname, sol ) 

def write_binary(file_name, u):
    '''
    Write the data in the proper binary format for vapor
    '''
    u.astype('float32').tofile(file_name)


# Run the main function
if __name__ == '__main__':
	main()

