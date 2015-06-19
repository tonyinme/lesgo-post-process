#!/usr/bin/python
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
import re
def main():
    # Read the input file 'lego.dat'
    print 'Converting files: '+ str(sys.argv[1:])

    # Establich number of files
    ts=len(sys.argv[1:])

    # Read the CGNS file
    for i, file_name in enumerate(sorted(sys.argv[1:], key=alphanum_key)):
        #~ print  file_name
        read_cgns(file_name,i,ts)

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)',s)]
   
def read_cgns(file_name,i,ts):
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
    
    for sol in f['/Base/Zone/Solution/']:
        print sol
        u = np.asarray(f['/Base/Zone/Solution/'+sol+'/ data'])
        create_vdf( sol , u,i,ts)

def create_vdf(file_name,u,i,ts):
    ''' 
    Write u array to a binary file and 
    use it to create VFD file from the 
    Vapor (NCAR) commands
    '''
    u.astype('float32').tofile(file_name)
    # minL used to scale dimension so the start at 1.0
    minL=min([L_x,L_y,L_z])
    cmd1=['vdfcreate -dimension '+str(N_x)+'x'+str(N_y) +'x'+str(N_z)+
        ' -numts '+ str(ts) +
        ' -level 0 -extents 0:0:0:'+str(L_x/minL)+
        ':'+str(L_y/minL)+':'+str(L_z/minL)+
        ' -vars3d '+file_name+' '+ file_name+'.vdf']
    cmd2=['raw2vdf -ts '+ str(i) +' -varname '+ file_name +' '+ file_name+'.vdf ' + file_name]

    while not os.path.isfile( file_name+'.vdf' ):
        os.system(cmd1[0])
        print cmd1[0]

    os.system(cmd2[0])
    print cmd2[0]
        



# Run the main function
if __name__ == '__main__':
	main()

