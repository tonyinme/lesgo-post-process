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
# Contains interpolation subroutines
# interp3(): function for interpolating linearly in 3D grid

import numpy as np

def interp3(x, y, z, u, xi, yi, zi):
    '''
    Interpolate 3D function
    x(nx),y(ny),z(nz),u(nx,ny,nz) are arrays
    xi yi zi are single numbers onto which to interpolate
    '''
    nz,ny,nx = np.shape(u)
    for i in range(nx-1):
        if x[i] <= xi and xi <= x[i+1]:
            i0=i
            i1=i+1
    for j in range(ny-1):
        if y[j] <= yi and yi <= y[j+1]:
            j0=j
            j1=j+1
    for k in range(nz-1):
        if z[k] <= zi and zi <= z[k+1]:
            k0=k
            k1=k+1
    xd=(xi-x[i0])/(x[i1]-x[i0])
    yd=(yi-y[j0])/(y[j1]-y[j0])
    zd=(zi-z[k0])/(z[k1]-z[k0])
    c00=u[k0,j0,i0]*(1.-xd)+u[k0,j0,i1]*xd
    c10=u[k0,j1,i0]*(1.-xd)+u[k0,j1,i1]*xd
    c01=u[k1,j0,i0]*(1.-xd)+u[k1,j0,i1]*xd
    c11=u[k1,j1,i0]*(1.-xd)+u[k1,j1,i1]*xd
    c0=c00*(1.-yd)+c10*yd
    c1=c01*(1.-yd)+c11*yd
    c=c0*(1.-zd)+c1*zd
    return c
