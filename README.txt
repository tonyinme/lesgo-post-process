==============================
Lesgo-post-process
==============================

Lesgo-post-process provides modules for dealing with CGNS data output from 
the LESGO Code. There are various capabilities in the module, but is meant to 
be used with CGNS output. The main language used is Python 2.7

The code provides a framework for getting data from CGNS output written
by the Johns Hopkins Turbulence Research Code LESGO.

Installation
==============================
# Dependencies:
# python 2.7, h5py, numpy

# Download from github:
git clone git@github.com:tonyinme/lesgo-post-process.git lesgo-post-process

# Go into directory
cd lesgo-post-process

# Install through python
sudo python setup.py install

Usage
==============================
The main utility can be accessed through the script:
-------
lesgopp
-------
This script takes as an input the name of the file to be used.
You will need an input file. 
The default and suggested name for it is: 'lesgo.data'
although you could potentially have a different name.

Here we provide an example for the file with an example dataset:

'lesgo.data'
================================================================================
# This file includes all the data that needs to be extracted from the 
# output files in the simulation
# The plots to include are sampling along a line of data
# The format to write this data is the following:
# name, point1, point2, N
# name (will become name of data file with .dat and plot name as .esp
# point1, point2 The points of the line
# N number of points to sample
#

# Line plots:
# The naming consists of parallalel axis to line, distance and, perpendicular 

# Directories to include
data_extract_location='./'
data_output_location='./Data'
plot_location='./plots'

extract_1D_data='yes'
extract_2D_data='yes'

plot_1D_data='yes'
plot_2D_data='yes'

# The fields need to specify various parameters:
# Name of variable; cgns file; label in latex format; min value; max value
fields:

VelocityX; veluv_avg.cgns; ${u}/{U_\infty}$; 0; 30.0

# Line data
# name; point 1; point 2; number of points along the line
1D_data:

line_a;[0.3,0.3,0.3];[1,1,1];20
line_b;[1.5,1.5,0.1];[1.5,1.5,1];25

# Planes
# Name of plane; normal to the plane; distance of the plane
2D_data:

# Clipping of domain
# clip = [x1, x2, y1, y2, z1, z2]
clip=[0, 3.14, 0, 3.14, 0, 1]

planeZ; normal='z', dis=0.5 
planeY; normal='y', dis=1.0
================================================================================

There is a script for post-processing the Actuator Turbine Model Output
-------
atmpp
-------
----------
'atmpp turbine1 turbine2'
--------
In order to run it you need to specify a list of turbine directories written
by the Actuator Turbine Model
It will time average the quantities along the blades such as lift and drag.
Also it will 

========================================
Vapor Data (https://www.vapor.ucar.edu/)
========================================
There are 2 scripts under bin which are meant to write Vapor data.
These scripts use the standard Vapor utilities so you will need to install those.

cgns_to_vdf: 
"cgns_to_vdf filename.cgns"
This is a python script which takes as an argument a CGNS file written by LESGO.
It will convert the CGNS file into a Vapor file.

video_cgns_to_vdf:
"video_cgns_to_vdf *.cgns"
This will take as an argument a set of CGNS files and write the collection
as a Vapor dataset.
You can open the vapor file and visualize the video automatically.

