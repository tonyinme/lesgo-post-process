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
# Module used for plotting


def combined_plot(compare_plot, params):
    '''
    Plot the list of combined files
    '''
    # Loop through all the files specified
    for field, items in labels.iteritems():
        plt.clf()
        for i, file_in in enumerate(params):
            plot_data=read_plot_file(file_in)
            x=plot_data['arclength']
            y=plot_data[field]
            plt.plot( x,y,dashes[i],color='black',label=file_in)
        plt.xlabel('arclength')
        plt.ylabel(field)
        #~ plt.legend(loc='best')
        # Place legend to the right
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # Save figure with legend
        plt.savefig('./plots/'+compare_plot+'-'+field+'.eps',bbox_inches='tight')

